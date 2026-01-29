import { useMemo, useState } from 'react';
import './App.css';

const initialState = {
  oid: '',
  title: '',
  created_at: '',
};

export default function App() {
  const [title, setTitle] = useState('');
  const [response, setResponse] = useState(initialState);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const hasResponse = useMemo(() => response.oid !== '', [response.oid]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setResponse(initialState);
    setLoading(true);

    try {
      const request = await fetch('/api/chats', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title }),
      });

      const payload = await request.json();

      if (!request.ok) {
        setError(payload?.detail ?? 'Не удалось создать чат.');
        return;
      }

      setResponse(payload);
      setTitle('');
    } catch (fetchError) {
      setError(fetchError?.message ?? 'Ошибка сети.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <main className="card">
        <header>
          <p className="eyebrow">FastAPI + Kafka chat</p>
          <h1>Создание чата</h1>
          <p className="subtitle">Введите название чата и отправьте запрос в API.</p>
        </header>

        <form onSubmit={handleSubmit} className="form">
          <label htmlFor="title">Название</label>
          <input
            id="title"
            name="title"
            type="text"
            placeholder="Например, Support"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Отправка...' : 'Создать чат'}
          </button>
        </form>

        {error && (
          <section className="panel error" role="alert">
            <h2>Ошибка</h2>
            <p>{error}</p>
          </section>
        )}

        {hasResponse && (
          <section className="panel success">
            <h2>Чат создан</h2>
            <dl>
              <div>
                <dt>ID</dt>
                <dd>{response.oid}</dd>
              </div>
              <div>
                <dt>Название</dt>
                <dd>{response.title}</dd>
              </div>
              <div>
                <dt>Создан</dt>
                <dd>{new Date(response.created_at).toLocaleString('ru-RU')}</dd>
              </div>
            </dl>
          </section>
        )}
      </main>
    </div>
  );
}
