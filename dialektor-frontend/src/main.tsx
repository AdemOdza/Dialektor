import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import '@mantine/core/styles.css';
import App from './App.tsx'
import { BrowserRouter, Routes, Route } from 'react-router'
import { MantineProvider } from '@mantine/core';

createRoot(document.getElementById('root')!).render(
  <MantineProvider>
  <StrictMode>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          {
          // For when we get to the word section: https://reactrouter.com/start/declarative/routing#dynamic-segments
          }
        </Routes>
      </BrowserRouter>
  </StrictMode>
  </MantineProvider>,
)
