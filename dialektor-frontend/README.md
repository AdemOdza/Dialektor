# Dialektor Frontend

A modern React.js frontend for Dialektor - an Albanian dialect dictionary website.

## Features

- **Modern Paper-like Theme**: Elegant design with cream/beige color palette
- **Sidebar Navigation**: Fixed left sidebar with logo, title, and navigation menu
- **Responsive Layout**: Clean, modern interface optimized for various screen sizes
- **Component-based Architecture**: Modular React components for maintainability

## Tech Stack

- **React** 19.1.1 - UI framework
- **Vite** 7.1.10 - Build tool and dev server
- **ESLint** - Code quality and linting

## Getting Started

### Prerequisites

- Node.js 20.x or higher
- npm 10.x or higher

### Installation

```bash
npm install
```

### Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Build

Create a production build:

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

Preview the production build locally:

```bash
npm run preview
```

### Linting

Run ESLint to check code quality:

```bash
npm run lint
```

## Project Structure

```
src/
├── components/
│   ├── Layout.jsx       # Main layout wrapper
│   ├── Layout.css
│   ├── Sidebar.jsx      # Left sidebar navigation
│   └── Sidebar.css
├── assets/              # Static assets
├── App.jsx              # Main application component
├── App.css
├── index.css            # Global styles
└── main.jsx             # Application entry point
```

## Color Palette

The application uses a modern paper-like color scheme:

- **Background**: `#fafaf8`, `#f0ede5` (light cream/beige gradients)
- **Sidebar**: `#f5f5f0`, `#ebe9e1` (slightly darker cream)
- **Accent**: `#8b7355`, `#6b563f` (earthy browns)
- **Text**: `#3e3528`, `#5a4d3d` (dark browns)
- **Borders**: `#d4d0c8` (subtle gray-brown)

## Contributing

1. Follow the existing code style
2. Run linting before committing: `npm run lint`
3. Test your changes: `npm run build`

