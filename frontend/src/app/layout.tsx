import React from 'react';
import { Metadata } from 'next';
import Navbar from '@/components/Navbar';
import { Toaster } from 'react-hot-toast';
import '@/styles/globals.css';

export const metadata: Metadata = {
  title: 'AI Interview Platform',
  description: 'Ace your interviews with AI-powered practice',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <main className="min-h-screen bg-gray-50">
          {children}
        </main>
        <Toaster />
      </body>
    </html>
  );
}
