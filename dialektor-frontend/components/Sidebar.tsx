'use client';

import Link from 'next/link';
import { useState } from 'react';

export default function Sidebar() {
  const [activeItem, setActiveItem] = useState('home');

  const menuItems = [
    { id: 'home', label: 'Home', href: '/' },
    { id: 'dialects', label: 'Dialects', href: '/dialects' },
    { id: 'words', label: 'Words', href: '/words' },
    { id: 'about', label: 'About', href: '/about' },
  ];

  return (
    <aside className="w-64 min-h-screen bg-white border-r border-gray-200 shadow-sm">
      {/* Logo Area */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-xl">D</span>
          </div>
          <h1 className="text-xl font-semibold text-gray-800">Dialektor</h1>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => (
            <li key={item.id}>
              <Link
                href={item.href}
                onClick={() => setActiveItem(item.id)}
                className={`block px-4 py-3 rounded-lg transition-all duration-200 ${
                  activeItem === item.id
                    ? 'bg-blue-50 text-blue-600 font-medium'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      {/* Footer Section */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 bg-white">
        <p className="text-xs text-gray-500 text-center">
          Albanian Language Dialects
        </p>
      </div>
    </aside>
  );
}
