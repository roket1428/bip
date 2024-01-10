import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { QueryClient } from '@tanstack/react-query';
import { PersistQueryClientProvider } from '@tanstack/react-query-persist-client';
import { createIDBPersister } from './persisters/createIDBPersister.tsx';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: Infinity,
      gcTime: Infinity,
    },
  },
})

const persister = createIDBPersister();
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <PersistQueryClientProvider client={queryClient} persistOptions={{ persister }}>
      <App queryClient={queryClient} />
    </PersistQueryClientProvider>
  </React.StrictMode>
);
