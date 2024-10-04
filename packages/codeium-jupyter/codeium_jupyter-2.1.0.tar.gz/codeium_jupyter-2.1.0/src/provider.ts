import {
  CompletionHandler,
  IInlineCompletionContext,
  IInlineCompletionProvider
} from '@jupyterlab/completer';

import { PromiseClient, createPromiseClient } from '@connectrpc/connect';
import { createConnectTransport } from '@connectrpc/connect-web';
import { IEditorLanguageRegistry } from '@jupyterlab/codemirror';
import { LanguageServerService } from './api/proto/exa/language_server_pb/language_server_connect';
import { PUBLIC_API_SERVER, PUBLIC_WEBSITE } from './urls';
import { registerUser } from './auth';
import { ContentsManager } from '@jupyterlab/services';

import { getCodeiumCompletions, simplifyCompletions } from './codeium';
import { v4 as uuidv4 } from 'uuid';

function isResponseError(
  error: any
): error is { response: { status: number } } {
  return error.response && typeof error.response.status === 'number';
}

// Note: some environments do not handle hidden directories, which is why
// we use codeium-jupyter instead of .codeium-jupyter
const SAVED_DIRECTORY = 'codeium-jupyter';
const SAVED_FILE = 'config.json';

interface Config {
  apiKey?: string;
  name?: string;
}

async function saveApiKeyAndName(config: Config) {
  const contents = new ContentsManager();

  // Ensure the directory exists
  try {
    await contents.get(SAVED_DIRECTORY, { type: 'directory' });
  } catch (error: unknown) {
    if (isResponseError(error) && error.response.status === 404) {
      // Create the directory if it doesn't exist
      await contents.save(SAVED_DIRECTORY, {
        type: 'directory',
        format: 'json',
        content: null
      });
    } else {
      throw error;
    }
  }

  const filePath = `${SAVED_DIRECTORY}/${SAVED_FILE}`;
  // Save the file with the API key content
  await contents.save(filePath, {
    type: 'file',
    format: 'text',
    content: JSON.stringify(config, null, 2) // Save the config
  });
}

function languageServerClient(
  baseUrl: string
): PromiseClient<typeof LanguageServerService> {
  const transport = createConnectTransport({
    baseUrl,
    useBinaryFormat: true
  });
  return createPromiseClient(LanguageServerService, transport);
}

export function getProfileUrl(portalUrl: string): string {
  if (portalUrl === '') {
    return PUBLIC_WEBSITE + '/profile';
  }
  return portalUrl.replace(/\/$/, '') + '/profile';
}

export function getAuthTokenUrl(portalUrl: string): string {
  const profileUrl = getProfileUrl(portalUrl);
  const params = new URLSearchParams({
    response_type: 'token',
    redirect_uri: 'chrome-show-auth-token',
    scope: 'openid profile email',
    prompt: 'login',
    redirect_parameters_type: 'query',
    state: uuidv4()
  });
  return `${profileUrl}?${params}`;
}

export function getApiServerUrl(portalUrl: string): string {
  if (portalUrl === '') {
    return PUBLIC_API_SERVER;
  }
  return `${portalUrl.replace(/\/$/, '')}/_route/api_server`;
}

export function getLanguageServerUrl(portalUrl: string): string {
  if (portalUrl === '') {
    return PUBLIC_API_SERVER;
  }
  return `${portalUrl.replace(/\/$/, '')}/_route/language_server`;
}

export class CodeiumProvider implements IInlineCompletionProvider {
  readonly identifier = 'codeium';
  readonly name = 'Codeium';

  constructor(options: CodeiumProvider.IOptions) {
    this._editorLanguageRegistry = options.editorLanguageRegistry;
    this._portalUrl = options.portalUrl;
    this._ideName = options.appname;
    this._ideVersion = options.version;
    this._client = languageServerClient(getApiServerUrl(options.portalUrl));
  }

  set portalUrl(portalUrl: string) {
    if (portalUrl === this._portalUrl) {
      // Do not show dialog if portalUrl is the same and api key is already set.
      if (this._apiKey !== '') {
        return;
      }
      // Load the api key from storage if it exists
      const contents = new ContentsManager();
      const filePath = `${SAVED_DIRECTORY}/${SAVED_FILE}`;
      contents
        .get(filePath)
        .then(file => {
          if (file !== null) {
            this._apiKey = file.content;
            console.log('API key loaded from storage');
            return;
          }
        })
        .catch(error => {
          console.error(error);
        });
    }
    this._portalUrl = portalUrl;
    this._client = languageServerClient(getLanguageServerUrl(portalUrl));
  }

  set authToken(authToken: string) {
    registerUser(authToken, getApiServerUrl(this._portalUrl))
      .then(apiKeyAndName => {
        this._apiKey = apiKeyAndName.api_key;
        saveApiKeyAndName({ apiKey: this._apiKey, name: apiKeyAndName.name })
          .then(() => {
            console.log('API key saved successfully!');
          })
          .catch(error => {
            console.error('Failed to save API key:', error);
          });
        console.log('Welcome,', apiKeyAndName.name);
      })
      .catch(error => console.error(error));
  }

  async fetch(
    request: CompletionHandler.IRequest,
    context: IInlineCompletionContext
  ) {
    const { text, offset: cursorOffset, mimeType } = request;
    const language = this._editorLanguageRegistry.findByMIME(mimeType ?? '');
    const results = await getCodeiumCompletions({
      client: this._client,
      text,
      cursorOffset,
      config: {
        apiKey: this._apiKey,
        language: language?.support?.language.name,
        ideName: this._ideName,
        ideVersion: this._ideVersion
      },
      otherDocuments: []
    });

    const simplified = simplifyCompletions(results).map(part => ({
      from: part.offset,
      to: part.offset,
      insert: part.completion
    }));

    // TODO(kevin): What were the offsets even for?
    return {
      items: simplified.map(part => ({ insertText: part.insert }))
    };
  }

  private _apiKey = '';
  private _portalUrl = '';
  private _ideName: string;
  private _ideVersion: string;

  private _editorLanguageRegistry: IEditorLanguageRegistry;
  private _client: PromiseClient<typeof LanguageServerService>;
}

export namespace CodeiumProvider {
  export interface IOptions {
    editorLanguageRegistry: IEditorLanguageRegistry;
    portalUrl: string;
    appname: string;
    version: string;
  }
}
