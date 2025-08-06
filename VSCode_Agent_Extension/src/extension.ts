import * as vscode from 'vscode';
import { app } from './agent';
import { HumanMessage, AIMessage, BaseMessage } from '@langchain/core/messages';

const CONVERSATION_HISTORY_KEY = 'conversationHistory';

function getWebviewContent(history: BaseMessage[]) {
  const messages = history.map(message => {
    const type = message instanceof HumanMessage ? 'user' : 'assistant';
    return `<div class="message ${type}-message">${message.content}</div>`;
  }).join('');

  return `<!DOCTYPE html>
  <html lang="en">
  <head>
	  <meta charset="UTF-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1.0">
	  <title>AI Assistant</title>
	  <style>
		  body {
			  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
			  margin: 0;
			  padding: 0;
			  display: flex;
			  flex-direction: column;
			  height: 100vh;
			  background-color: var(--vscode-editor-background);
			  color: var(--vscode-editor-foreground);
		  }
		  #messages {
			  flex: 1;
			  padding: 10px;
			  overflow-y: auto;
		  }
		  .message {
			  margin-bottom: 10px;
			  padding: 8px 12px;
			  border-radius: 18px;
			  max-width: 80%;
			  word-wrap: break-word;
		  }
		  .user-message {
			  background-color: var(--vscode-button-background);
			  align-self: flex-end;
			  margin-left: auto;
		  }
		  .assistant-message {
			  background-color: var(--vscode-input-background);
			  align-self: flex-start;
		  }
		  #input-area {
			  display: flex;
			  padding: 10px;
			  border-top: 1px solid var(--vscode-editor-background);
		  }
		  #user-input {
			  flex: 1;
			  border: none;
			  padding: 10px;
			  border-radius: 5px;
			  background-color: var(--vscode-input-background);
			  color: var(--vscode-input-foreground);
		  }
		  #user-input:focus {
			  outline: 1px solid var(--vscode-focusBorder);
		  }
		  button {
			  margin-left: 10px;
			  padding: 10px 15px;
			  border: none;
			  background-color: var(--vscode-button-background);
			  color: var(--vscode-button-foreground);
			  border-radius: 5px;
			  cursor: pointer;
		  }
		  button:hover {
			  background-color: var(--vscode-button-hoverBackground);
		  }
	  </style>
  </head>
  <body>
	  <div id="messages">${messages}</div>
	  <div id="input-area">
		  <input type="text" id="user-input" placeholder="Ask a question...">
		  <button id="send-button">Send</button>
	  </div>
	  <script>
		  const vscode = acquireVsCodeApi();
		  const messagesDiv = document.getElementById('messages');
		  const userInput = document.getElementById('user-input');
		  const sendButton = document.getElementById('send-button');

		  messagesDiv.scrollTop = messagesDiv.scrollHeight;

		  sendButton.addEventListener('click', sendMessage);
		  userInput.addEventListener('keyup', (event) => {
			  if (event.key === 'Enter') {
				  sendMessage();
			  }
		  });

		  function sendMessage() {
			  const text = userInput.value;
			  if (text.trim() === '') return;

			  addMessage('user', text);
			  vscode.postMessage({
				  command: 'user-message',
				  text: text
			  });
			  userInput.value = '';
		  }

		  function addMessage(sender, text) {
			  const message = document.createElement('div');
			  message.classList.add('message', sender + '-message');
			  message.textContent = text;
			  messagesDiv.appendChild(message);
			  messagesDiv.scrollTop = messagesDiv.scrollHeight;
		  }

		  window.addEventListener('message', event => {
			  const message = event.data;
			  switch (message.command) {
				  case 'assistant-message':
					  addMessage('assistant', message.text);
					  break;
			  }
		  });
	  </script>
  </body>
  </html>`;
}

export function activate(context: vscode.ExtensionContext) {
  let history: BaseMessage[] = context.globalState.get(CONVERSATION_HISTORY_KEY, []);

  let disposable = vscode.commands.registerCommand('vscode-agent-extension.start', () => {
    const panel = vscode.window.createWebviewPanel(
      'aiAssistant',
      'AI Assistant',
      vscode.ViewColumn.Two,
      {
        enableScripts: true,
        localResourceRoots: [vscode.Uri.joinPath(context.extensionUri, 'dist')]
      }
    );

    panel.webview.html = getWebviewContent(history);

    panel.onDidDispose(() => {
        context.globalState.update(CONVERSATION_HISTORY_KEY, history);
    });

    panel.webview.onDidReceiveMessage(
      async (message: { command: string; text: string }) => {
        switch (message.command) {
          case 'user-message':
            const userMessage = new HumanMessage(message.text);
            history.push(userMessage);

            const result = await app.invoke({ messages: history });
            const assistantResponse = result.messages[result.messages.length - 1];
            history.push(assistantResponse);

            panel.webview.postMessage({ command: 'assistant-message', text: assistantResponse.content });
            return;
        }
      },
      undefined,
      context.subscriptions
    );
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}
