import { useEffect, useMemo, useState } from 'react';
import './App.css';

const VISITOR_PREFIX = 'VISITOR:';
const ADMIN_PREFIX = 'ADMIN:';
const STORAGE_KEY = 'fastchat-demo-chat-id';

async function requestJson(url, options) {
  const response = await fetch(url, options);
  const payload = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(payload?.detail ?? 'Request failed');
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

function sortChats(chats) {
  return [...chats].sort((left, right) => new Date(right.created_at) - new Date(left.created_at));
}

function sortMessages(messages = []) {
  return [...messages].sort((left, right) => new Date(left.created_at) - new Date(right.created_at));
}

function parseMessage(message) {
  const text = message.text ?? '';

  if (text.startsWith(VISITOR_PREFIX)) {
    return { role: 'visitor', text: text.slice(VISITOR_PREFIX.length).trim() };
  }

  if (text.startsWith(ADMIN_PREFIX)) {
    return { role: 'admin', text: text.slice(ADMIN_PREFIX.length).trim() };
  }

  return { role: 'system', text };
}

function readStoredChatId() {
  try {
    return window.localStorage.getItem(STORAGE_KEY);
  } catch {
    return null;
  }
}

function storeChatId(chatId) {
  try {
    window.localStorage.setItem(STORAGE_KEY, chatId);
  } catch {
    // Local storage is optional for the demo flow.
  }
}

function ChatMessages({ chat, emptyTitle, emptyCopy }) {
  const messages = useMemo(() => sortMessages(chat?.messages), [chat?.messages]);

  if (!chat) {
    return (
      <div className="dock-empty">
        <strong>{emptyTitle}</strong>
        <span>{emptyCopy}</span>
      </div>
    );
  }

  if (messages.length === 0) {
    return (
      <div className="dock-empty">
        <strong>No messages</strong>
        <span>Start with one short line.</span>
      </div>
    );
  }

  return (
    <div className="message-stack">
      {messages.map((message) => {
        const parsed = parseMessage(message);

        return (
          <article className={`bubble bubble-${parsed.role}`} key={message.oid}>
            <p>{parsed.text}</p>
            <time dateTime={message.created_at}>{formatTime(message.created_at)}</time>
          </article>
        );
      })}
    </div>
  );
}

function VisitorSite({ onAdminClick }) {
  return (
    <main className="site-page">
      <header className="site-nav">
        <a className="site-wordmark" href="#top" aria-label="Cinder Field">
          <span>CF</span>
          <strong>Cinder Field</strong>
        </a>
        <nav className="site-links" aria-label="Primary">
          <a href="#work">Work</a>
          <a href="#process">Process</a>
          <a href="#notes">Notes</a>
        </nav>
        <button className="nav-admin" type="button" onClick={onAdminClick}>
          Admin
        </button>
      </header>

      <section className="hero-grid" id="top">
        <div className="hero-copy">
          <p className="kicker">Field systems and odd commerce</p>
          <h1>Plain tools for teams that move fast.</h1>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat at
            ante venenatis dapibus posuere velit aliquet.
          </p>
          <div className="hero-actions">
            <a href="#work">Read brief</a>
            <a href="#notes">Open notes</a>
          </div>
        </div>

        <div className="mock-poster" aria-label="Editorial product visual">
          <div className="poster-band">SYSTEM BOARD</div>
          <div className="poster-grid">
            <span>01</span>
            <span>17</span>
            <span>43</span>
            <span>89</span>
          </div>
          <div className="poster-foot">NORTH DOCK</div>
        </div>
      </section>

      <section className="content-band" id="work">
        <article>
          <span>01</span>
          <h2>Stock rhythm</h2>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sed odio dui. Cras
            justo odio, dapibus ac facilisis in, egestas eget quam.
          </p>
        </article>
        <article>
          <span>02</span>
          <h2>Order desk</h2>
          <p>
            Vestibulum id ligula porta felis euismod semper. Nullam quis risus eget urna mollis
            ornare vel eu leo.
          </p>
        </article>
        <article>
          <span>03</span>
          <h2>Routing</h2>
          <p>
            Maecenas faucibus mollis interdum. Aenean lacinia bibendum nulla sed consectetur.
          </p>
        </article>
      </section>

      <section className="split-band" id="process">
        <div>
          <h2>Operations without the ceremony.</h2>
        </div>
        <p>
          Morbi leo risus, porta ac consectetur ac, vestibulum at eros. Etiam porta sem malesuada
          magna mollis euismod. Sed posuere consectetur est at lobortis.
        </p>
      </section>
    </main>
  );
}

function AdminSite({ onSiteClick }) {
  return (
    <main className="admin-page">
      <header className="admin-nav">
        <div>
          <span className="admin-mark">FC</span>
          <strong>FastChat Admin</strong>
        </div>
        <button className="nav-admin" type="button" onClick={onSiteClick}>
          Site
        </button>
      </header>

      <section className="admin-shell">
        <div className="admin-headline">
          <p className="kicker">Control room</p>
          <h1>Inbox, service status, and site telemetry.</h1>
        </div>

        <div className="admin-metrics">
          <article>
            <span>Live chats</span>
            <strong>03</strong>
          </article>
          <article>
            <span>Median reply</span>
            <strong>02m</strong>
          </article>
          <article>
            <span>Queue load</span>
            <strong>Low</strong>
          </article>
        </div>

        <div className="admin-table" aria-label="Recent events">
          <div>
            <span>09:14</span>
            <strong>New visitor session</strong>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
          </div>
          <div>
            <span>09:22</span>
            <strong>Operator assigned</strong>
            <p>Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor.</p>
          </div>
          <div>
            <span>09:31</span>
            <strong>Reply drafted</strong>
            <p>Integer posuere erat a ante venenatis dapibus posuere velit aliquet.</p>
          </div>
        </div>
      </section>
    </main>
  );
}

function VisitorDock({
  chat,
  isOpen,
  isSending,
  isBooting,
  messageText,
  error,
  onOpen,
  onClose,
  onTextChange,
  onSubmit,
}) {
  if (!isOpen) {
    return (
      <button className="chat-launcher" type="button" onClick={onOpen} aria-label="Open chat">
        CHAT
      </button>
    );
  }

  return (
    <aside className="chat-dock visitor-dock" aria-label="Website chat">
      <header className="dock-header">
        <div>
          <span>Live desk</span>
          <strong>Support</strong>
        </div>
        <button type="button" onClick={onClose} aria-label="Close chat">
          X
        </button>
      </header>

      {error && <div className="dock-error">{error}</div>}

      <ChatMessages
        chat={chat}
        emptyTitle={isBooting ? 'Opening chat' : 'Say hello'}
        emptyCopy={isBooting ? 'Preparing the desk.' : 'A short message is enough.'}
      />

      <form className="dock-composer" onSubmit={onSubmit}>
        <input
          type="text"
          maxLength={4000}
          placeholder="Type message"
          value={messageText}
          onChange={(event) => onTextChange(event.target.value)}
          disabled={isSending || isBooting}
        />
        <button type="submit" disabled={isSending || isBooting || !messageText.trim()}>
          {isSending ? '...' : 'Send'}
        </button>
      </form>
    </aside>
  );
}

function AdminDock({
  chats,
  activeChat,
  isOpen,
  isSending,
  isLoading,
  messageText,
  error,
  onOpen,
  onClose,
  onSelectChat,
  onTextChange,
  onSubmit,
}) {
  const sortedChats = useMemo(() => sortChats(chats), [chats]);

  if (!isOpen) {
    return (
      <button className="chat-launcher admin-launcher" type="button" onClick={onOpen} aria-label="Open inbox">
        INBOX
      </button>
    );
  }

  return (
    <aside className="chat-dock admin-dock" aria-label="Admin inbox">
      <header className="dock-header">
        <div>
          <span>Operator desk</span>
          <strong>{activeChat?.title ?? 'Inbox'}</strong>
        </div>
        <button type="button" onClick={onClose} aria-label="Close inbox">
          X
        </button>
      </header>

      {error && <div className="dock-error">{error}</div>}

      <div className="admin-chat-layout">
        <div className="dock-list" aria-label="Chats">
          {isLoading && <span className="list-note">Loading</span>}
          {!isLoading && sortedChats.length === 0 && <span className="list-note">No chats</span>}
          {sortedChats.map((chat) => (
            <button
              className={chat.oid === activeChat?.oid ? 'selected' : ''}
              key={chat.oid}
              type="button"
              onClick={() => onSelectChat(chat.oid)}
            >
              <strong>{chat.title}</strong>
              <span>{formatTime(chat.created_at)}</span>
            </button>
          ))}
        </div>

        <div className="admin-thread">
          <ChatMessages
            chat={activeChat}
            emptyTitle="Select chat"
            emptyCopy="Visitor messages appear here."
          />

          <form className="dock-composer" onSubmit={onSubmit}>
            <input
              type="text"
              maxLength={4000}
              placeholder={activeChat ? 'Reply' : 'Select chat first'}
              value={messageText}
              onChange={(event) => onTextChange(event.target.value)}
              disabled={!activeChat || isSending}
            />
            <button type="submit" disabled={!activeChat || isSending || !messageText.trim()}>
              {isSending ? '...' : 'Reply'}
            </button>
          </form>
        </div>
      </div>
    </aside>
  );
}

export default function App() {
  const [view, setView] = useState(() => (window.location.hash === '#admin' ? 'admin' : 'site'));
  const [chats, setChats] = useState([]);
  const [visitorChat, setVisitorChat] = useState(null);
  const [adminChat, setAdminChat] = useState(null);
  const [visitorDockOpen, setVisitorDockOpen] = useState(false);
  const [adminDockOpen, setAdminDockOpen] = useState(false);
  const [visitorText, setVisitorText] = useState('');
  const [adminText, setAdminText] = useState('');
  const [error, setError] = useState('');
  const [isBootingVisitor, setIsBootingVisitor] = useState(false);
  const [isLoadingChats, setIsLoadingChats] = useState(false);
  const [isVisitorSending, setIsVisitorSending] = useState(false);
  const [isAdminSending, setIsAdminSending] = useState(false);

  const sortedChats = useMemo(() => sortChats(chats), [chats]);

  const loadChat = async (chatId) => requestJson(`/api/chats/${chatId}`);

  const loadChats = async () => {
    setIsLoadingChats(true);

    try {
      const payload = await requestJson('/api/chats');
      setChats(payload);
      return payload;
    } finally {
      setIsLoadingChats(false);
    }
  };

  const createVisitorChat = async () => {
    const suffix = Math.random().toString(36).slice(2, 6).toUpperCase();
    const title = `Website visitor ${new Intl.DateTimeFormat('en-GB', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    }).format(new Date())} ${suffix}`;

    const chat = await requestJson('/api/chats', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title }),
    });

    const nextChat = { ...chat, messages: [] };
    storeChatId(chat.oid);
    setVisitorChat(nextChat);
    setChats((current) => [chat, ...current.filter((item) => item.oid !== chat.oid)]);
    return nextChat;
  };

  const ensureVisitorChat = async () => {
    if (visitorChat?.oid) {
      return visitorChat;
    }

    const storedChatId = readStoredChatId();

    if (storedChatId) {
      try {
        const storedChat = await loadChat(storedChatId);
        setVisitorChat(storedChat);
        return storedChat;
      } catch {
        storeChatId('');
      }
    }

    return createVisitorChat();
  };

  const openVisitorDock = async () => {
    setVisitorDockOpen(true);
    setError('');
    setIsBootingVisitor(true);

    try {
      await ensureVisitorChat();
    } catch (fetchError) {
      setError(fetchError?.message ?? 'Chat is not available');
    } finally {
      setIsBootingVisitor(false);
    }
  };

  const openAdminDock = async () => {
    setAdminDockOpen(true);
    setError('');

    try {
      const payload = await loadChats();
      const preferredChatId = visitorChat?.oid ?? readStoredChatId() ?? sortChats(payload)[0]?.oid;

      if (preferredChatId) {
        const selectedChat = await loadChat(preferredChatId);
        setAdminChat(selectedChat);
      }
    } catch (fetchError) {
      setError(fetchError?.message ?? 'Inbox is not available');
    }
  };

  const selectAdminChat = async (chatId) => {
    setError('');

    try {
      const selectedChat = await loadChat(chatId);
      setAdminChat(selectedChat);
    } catch (fetchError) {
      setError(fetchError?.message ?? 'Chat is not available');
    }
  };

  const sendMessage = async (chatId, rolePrefix, text) =>
    requestJson(`/api/chats/${chatId}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: `${rolePrefix} ${text.trim()}` }),
    });

  const handleVisitorSubmit = async (event) => {
    event.preventDefault();

    if (!visitorText.trim()) {
      return;
    }

    setIsVisitorSending(true);
    setError('');

    try {
      const chat = await ensureVisitorChat();
      const message = await sendMessage(chat.oid, VISITOR_PREFIX, visitorText);
      const nextChat = { ...chat, messages: [...(chat.messages ?? []), message] };
      setVisitorChat(nextChat);
      setVisitorText('');

      if (adminChat?.oid === chat.oid) {
        setAdminChat(nextChat);
      }

      await loadChats();
    } catch (fetchError) {
      setError(fetchError?.message ?? 'Message was not sent');
    } finally {
      setIsVisitorSending(false);
    }
  };

  const handleAdminSubmit = async (event) => {
    event.preventDefault();

    if (!adminChat?.oid || !adminText.trim()) {
      return;
    }

    setIsAdminSending(true);
    setError('');

    try {
      const message = await sendMessage(adminChat.oid, ADMIN_PREFIX, adminText);
      const nextChat = { ...adminChat, messages: [...(adminChat.messages ?? []), message] };
      setAdminChat(nextChat);
      setAdminText('');

      if (visitorChat?.oid === adminChat.oid) {
        setVisitorChat(nextChat);
      }

      await loadChats();
    } catch (fetchError) {
      setError(fetchError?.message ?? 'Reply was not sent');
    } finally {
      setIsAdminSending(false);
    }
  };

  const goAdmin = async () => {
    window.location.hash = 'admin';
    setView('admin');
    setVisitorDockOpen(false);
    await openAdminDock();
  };

  const goSite = () => {
    window.history.pushState('', document.title, window.location.pathname + window.location.search);
    setView('site');
    setAdminDockOpen(false);
  };

  useEffect(() => {
    const syncViewFromHash = () => {
      setView(window.location.hash === '#admin' ? 'admin' : 'site');
    };

    window.addEventListener('hashchange', syncViewFromHash);
    return () => window.removeEventListener('hashchange', syncViewFromHash);
  }, []);

  useEffect(() => {
    loadChats().catch((fetchError) => setError(fetchError?.message ?? 'Chats are not available'));

    const storedChatId = readStoredChatId();
    if (storedChatId) {
      loadChat(storedChatId)
        .then((chat) => setVisitorChat(chat))
        .catch(() => storeChatId(''));
    }
  }, []);

  useEffect(() => {
    if (!visitorDockOpen && !adminDockOpen) {
      return undefined;
    }

    const intervalId = window.setInterval(async () => {
      try {
        const payload = await requestJson('/api/chats');
        setChats(payload);

        if (visitorDockOpen) {
          const visitorChatId = visitorChat?.oid ?? readStoredChatId();
          if (visitorChatId) {
            setVisitorChat(await loadChat(visitorChatId));
          }
        }

        if (adminDockOpen) {
          const adminChatId = adminChat?.oid ?? visitorChat?.oid ?? sortedChats[0]?.oid;
          if (adminChatId) {
            setAdminChat(await loadChat(adminChatId));
          }
        }
      } catch {
        // The next manual action will surface a visible error.
      }
    }, 3000);

    return () => window.clearInterval(intervalId);
  }, [visitorDockOpen, adminDockOpen, visitorChat?.oid, adminChat?.oid, sortedChats]);

  return (
    <div className="app-shell">
      {view === 'admin' ? <AdminSite onSiteClick={goSite} /> : <VisitorSite onAdminClick={goAdmin} />}

      {view === 'admin' ? (
        <AdminDock
          chats={chats}
          activeChat={adminChat}
          isOpen={adminDockOpen}
          isSending={isAdminSending}
          isLoading={isLoadingChats}
          messageText={adminText}
          error={error}
          onOpen={openAdminDock}
          onClose={() => setAdminDockOpen(false)}
          onSelectChat={selectAdminChat}
          onTextChange={setAdminText}
          onSubmit={handleAdminSubmit}
        />
      ) : (
        <VisitorDock
          chat={visitorChat}
          isOpen={visitorDockOpen}
          isSending={isVisitorSending}
          isBooting={isBootingVisitor}
          messageText={visitorText}
          error={error}
          onOpen={openVisitorDock}
          onClose={() => setVisitorDockOpen(false)}
          onTextChange={setVisitorText}
          onSubmit={handleVisitorSubmit}
        />
      )}
    </div>
  );
}
