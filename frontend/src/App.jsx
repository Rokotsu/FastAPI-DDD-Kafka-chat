import { useEffect, useMemo, useState } from 'react';
import './App.css';

const defaultChatTitle = 'Website support';

async function requestJson(url, options) {
  const response = await fetch(url, options);
  const payload = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(payload?.detail ?? 'Request failed.');
  }

  return payload;
}

function formatTime(value) {
  if (!value) {
    return '';
  }

  return new Intl.DateTimeFormat('ru-RU', {
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value));
}

export default function App() {
  const [chatTitle, setChatTitle] = useState(defaultChatTitle);
  const [messageText, setMessageText] = useState('');
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);
  const [error, setError] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [isLoadingChats, setIsLoadingChats] = useState(true);

  const activeChatId = activeChat?.oid ?? '';
  const sortedChats = useMemo(
    () => [...chats].sort((left, right) => new Date(right.created_at) - new Date(left.created_at)),
    [chats],
  );
  const messages = useMemo(
    () => [...(activeChat?.messages ?? [])].sort((left, right) => new Date(left.created_at) - new Date(right.created_at)),
    [activeChat?.messages],
  );

  const loadChat = async (chatId) => {
    const chat = await requestJson(`/api/chats/${chatId}`);
    setActiveChat(chat);
    return chat;
  };

  const loadChats = async () => {
    setError('');
    setIsLoadingChats(true);

    try {
      const payload = await requestJson('/api/chats');
      setChats(payload);

      if (payload.length > 0) {
        await loadChat(payload[payload.length - 1].oid);
      }
    } catch (fetchError) {
      setError(fetchError?.message ?? 'Не удалось загрузить чаты.');
    } finally {
      setIsLoadingChats(false);
    }
  };

  useEffect(() => {
    loadChats();
  }, []);

  const handleCreateChat = async (event) => {
    event.preventDefault();
    setError('');
    setIsCreating(true);

    try {
      const chat = await requestJson('/api/chats', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: chatTitle.trim() }),
      });

      setChats((current) => [...current, chat]);
      setActiveChat({ ...chat, messages: [] });
      setChatTitle('');
    } catch (fetchError) {
      setError(fetchError?.message ?? 'Не удалось создать чат.');
    } finally {
      setIsCreating(false);
    }
  };

  const handleSendMessage = async (event) => {
    event.preventDefault();

    if (!activeChatId || !messageText.trim()) {
      return;
    }

    setError('');
    setIsSending(true);

    try {
      const message = await requestJson(`/api/chats/${activeChatId}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: messageText.trim() }),
      });

      setActiveChat((current) => ({
        ...current,
        messages: [...(current?.messages ?? []), message],
      }));
      setMessageText('');
    } catch (fetchError) {
      setError(fetchError?.message ?? 'Не удалось отправить сообщение.');
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="app">
      <header className="site-header">
        <span className="brand-mark">FC</span>
        <strong>FastChat Embed</strong>
      </header>

      <main className="workspace">
        <aside className="sidebar">
          <form className="create-form" onSubmit={handleCreateChat}>
            <label htmlFor="chat-title">Новый чат</label>
            <div className="input-row">
              <input
                id="chat-title"
                type="text"
                maxLength={255}
                placeholder="Например, отдел продаж"
                value={chatTitle}
                onChange={(event) => setChatTitle(event.target.value)}
                required
              />
              <button type="submit" disabled={isCreating}>
                {isCreating ? '...' : '+'}
              </button>
            </div>
          </form>

          <div className="chat-list" aria-label="Список чатов">
            {isLoadingChats && <p className="muted">Загрузка...</p>}
            {!isLoadingChats && sortedChats.length === 0 && (
              <p className="muted">Создайте первый чат.</p>
            )}
            {sortedChats.map((chat) => (
              <button
                className={`chat-item ${chat.oid === activeChatId ? 'active' : ''}`}
                key={chat.oid}
                type="button"
                onClick={() => loadChat(chat.oid).catch((fetchError) => setError(fetchError.message))}
              >
                <span>{chat.title}</span>
                <small>{formatTime(chat.created_at)}</small>
              </button>
            ))}
          </div>
        </aside>

        <section className="chat-panel" aria-live="polite">
          <div className="chat-header">
            <div>
              <p className="eyebrow">Embedded website chat</p>
              <h1>{activeChat?.title ?? 'Чат для сайта'}</h1>
            </div>
            <span className="status">online</span>
          </div>

          {error && (
            <div className="error" role="alert">
              {error}
            </div>
          )}

          <div className="messages">
            {!activeChat && (
              <div className="empty-state">
                <h2>Выберите чат или создайте новый</h2>
                <p>После этого здесь появится история сообщений.</p>
              </div>
            )}

            {activeChat && messages.length === 0 && (
              <div className="empty-state">
                <h2>Сообщений пока нет</h2>
                <p>Отправьте первое сообщение в выбранный чат.</p>
              </div>
            )}

            {messages.map((message) => (
              <article className="message" key={message.oid}>
                <p>{message.text}</p>
                <time dateTime={message.created_at}>{formatTime(message.created_at)}</time>
              </article>
            ))}
          </div>

          <form className="composer" onSubmit={handleSendMessage}>
            <input
              type="text"
              maxLength={4000}
              placeholder={activeChat ? 'Введите сообщение...' : 'Сначала выберите чат'}
              value={messageText}
              onChange={(event) => setMessageText(event.target.value)}
              disabled={!activeChat || isSending}
            />
            <button type="submit" disabled={!activeChat || isSending || !messageText.trim()}>
              {isSending ? '...' : 'Отправить'}
            </button>
          </form>
        </section>
      </main>
    </div>
  );
}
