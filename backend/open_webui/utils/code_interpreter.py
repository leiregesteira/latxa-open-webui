import asyncio
import base64
import io
import json
import logging
import uuid
from typing import Optional

import aiohttp
import websockets
from open_webui.env import AIOHTTP_CLIENT_ALLOW_REDIRECTS
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ResultModel(BaseModel):
    """
    Execute Code Result Model
    """

    stdout: Optional[str] = ''
    stderr: Optional[str] = ''
    result: Optional[str] = ''
    files: Optional[list[dict]] = None


class JupyterCodeExecuter:
    """
    Execute code in jupyter notebook
    """

    def __init__(
        self,
        base_url: str,
        code: str,
        token: str = '',
        password: str = '',
        timeout: int = 60,
        user=None,
    ):
        """
        :param base_url: Jupyter server URL (e.g., "http://localhost:8888")
        :param code: Code to execute
        :param token: Jupyter authentication token (optional)
        :param password: Jupyter password (optional)
        :param timeout: WebSocket timeout in seconds (default: 60s)
        :param user: authenticated user, used to own any files the executed code creates
        """
        self.base_url = base_url
        self.code = code
        self.token = token
        self.password = password
        self.timeout = timeout
        self.user = user
        self.kernel_id = ''
        if self.base_url[-1] != '/':
            self.base_url += '/'
        self.session = aiohttp.ClientSession(trust_env=True, base_url=self.base_url)
        self.params = {}
        self.result = ResultModel()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.kernel_id:
            try:
                async with self.session.delete(f'api/kernels/{self.kernel_id}', params=self.params) as response:
                    response.raise_for_status()
            except Exception as err:
                logger.exception('close kernel failed, %s', err)
        await self.session.close()

    async def run(self) -> ResultModel:
        try:
            await self.sign_in()
            await self.init_kernel()
            files_before = await self.list_workspace_files()
            await self.execute_code()
            files_after = await self.list_workspace_files()
            await self.collect_created_files(files_before, files_after)
        except Exception as err:
            logger.exception('execute code failed, %s', err)
            self.result.stderr = f'Error: {err}'
        return self.result

    async def list_workspace_files(self) -> dict:
        """List files in the kernel's working directory (Jupyter Contents API), keyed by path."""
        try:
            async with self.session.get('api/contents', params=self.params) as response:
                response.raise_for_status()
                listing = await response.json()
        except Exception as err:
            logger.warning('could not list jupyter workspace files, %s', err)
            return {}

        return {
            item['path']: item.get('last_modified')
            for item in listing.get('content', [])
            if item.get('type') == 'file'
        }

    async def collect_created_files(self, files_before: dict, files_after: dict) -> None:
        """Detect files newly created or modified by the executed code and store them as downloadable files."""
        if self.user is None:
            return

        new_or_changed = [
            path
            for path, last_modified in files_after.items()
            if path not in files_before or files_before[path] != last_modified
        ]
        if not new_or_changed:
            return

        # Deferred imports: this module doesn't otherwise depend on the app's storage/db layer.
        from open_webui.models.files import FileForm, Files
        from open_webui.storage.provider import Storage

        stored_files = []
        for path in new_or_changed:
            try:
                async with self.session.get(f'api/contents/{path}', params=self.params) as response:
                    response.raise_for_status()
                    file_data = await response.json()

                if file_data.get('type') != 'file':
                    continue

                content = file_data.get('content', '')
                if file_data.get('format') == 'base64':
                    raw_bytes = base64.b64decode(content)
                else:
                    raw_bytes = content.encode('utf-8')

                name = path.rsplit('/', 1)[-1]
                file_id = str(uuid.uuid4())
                storage_filename = f'{file_id}_{name}'
                tags = {'OpenWebUI-File-Id': file_id, 'OpenWebUI-User-Id': self.user.id}

                _, file_path = await asyncio.to_thread(
                    Storage.upload_file, io.BytesIO(raw_bytes), storage_filename, tags
                )

                await Files.insert_new_file(
                    self.user.id,
                    FileForm(
                        id=file_id,
                        filename=name,
                        path=file_path,
                        data={},
                        meta={
                            'name': name,
                            'content_type': file_data.get('mimetype'),
                            'size': len(raw_bytes),
                        },
                    ),
                )

                stored_files.append({'id': file_id, 'name': name, 'url': f'/api/v1/files/{file_id}/content'})
            except Exception as err:
                logger.warning('could not store code-execution output file %s, %s', path, err)

        if stored_files:
            self.result.files = stored_files

    async def sign_in(self) -> None:
        # password authentication
        if self.password and not self.token:
            async with self.session.get('login') as response:
                response.raise_for_status()
                xsrf_token = response.cookies['_xsrf'].value
                if not xsrf_token:
                    raise ValueError('_xsrf token not found')
                self.session.cookie_jar.update_cookies(response.cookies)
                self.session.headers.update({'X-XSRFToken': xsrf_token})
            async with self.session.post(
                'login',
                data={'_xsrf': xsrf_token, 'password': self.password},
                allow_redirects=AIOHTTP_CLIENT_ALLOW_REDIRECTS,
            ) as response:
                response.raise_for_status()
                self.session.cookie_jar.update_cookies(response.cookies)

        # token authentication
        if self.token:
            self.params.update({'token': self.token})

    async def init_kernel(self) -> None:
        async with self.session.post(url='api/kernels', params=self.params) as response:
            response.raise_for_status()
            kernel_data = await response.json()
            self.kernel_id = kernel_data['id']

    def init_ws(self) -> (str, dict):
        ws_base = self.base_url.replace('http', 'ws', 1)
        ws_params = '?' + '&'.join([f'{key}={val}' for key, val in self.params.items()])
        websocket_url = f'{ws_base}api/kernels/{self.kernel_id}/channels{ws_params if len(ws_params) > 1 else ""}'
        ws_headers = {}
        if self.password and not self.token:
            ws_headers = {
                'Cookie': '; '.join([f'{cookie.key}={cookie.value}' for cookie in self.session.cookie_jar]),
                **self.session.headers,
            }
        return websocket_url, ws_headers

    async def execute_code(self) -> None:
        # initialize ws
        websocket_url, ws_headers = self.init_ws()
        # execute
        async with websockets.connect(websocket_url, additional_headers=ws_headers) as ws:
            await self.execute_in_jupyter(ws)

    async def execute_in_jupyter(self, ws) -> None:
        # send message
        msg_id = uuid.uuid4().hex
        await ws.send(
            json.dumps(
                {
                    'header': {
                        'msg_id': msg_id,
                        'msg_type': 'execute_request',
                        'username': 'user',
                        'session': uuid.uuid4().hex,
                        'date': '',
                        'version': '5.3',
                    },
                    'parent_header': {},
                    'metadata': {},
                    'content': {
                        'code': self.code,
                        'silent': False,
                        'store_history': True,
                        'user_expressions': {},
                        'allow_stdin': False,
                        'stop_on_error': True,
                    },
                    'channel': 'shell',
                }
            )
        )
        # parse message
        stdout, stderr, result = '', '', []
        while True:
            try:
                # wait for message
                message = await asyncio.wait_for(ws.recv(), self.timeout)
                message_data = json.loads(message)
                # msg id not match, skip
                if message_data.get('parent_header', {}).get('msg_id') != msg_id:
                    continue
                # check message type
                msg_type = message_data.get('msg_type')
                match msg_type:
                    case 'stream':
                        if message_data['content']['name'] == 'stdout':
                            stdout += message_data['content']['text']
                        elif message_data['content']['name'] == 'stderr':
                            stderr += message_data['content']['text']
                    case 'execute_result' | 'display_data':
                        data = message_data['content']['data']
                        if 'image/png' in data:
                            result.append(f'data:image/png;base64,{data["image/png"]}')
                        elif 'text/plain' in data:
                            result.append(data['text/plain'])
                    case 'error':
                        stderr += '\n'.join(message_data['content']['traceback'])
                    case 'status':
                        if message_data['content']['execution_state'] == 'idle':
                            break

            except asyncio.TimeoutError:
                stderr += '\nExecution timed out.'
                break
        self.result.stdout = stdout.strip()
        self.result.stderr = stderr.strip()
        self.result.result = '\n'.join(result).strip() if result else ''


async def execute_code_jupyter(
    base_url: str, code: str, token: str = '', password: str = '', timeout: int = 60, user=None
) -> dict:
    async with JupyterCodeExecuter(base_url, code, token, password, timeout, user=user) as executor:
        result = await executor.run()
        return result.model_dump()
