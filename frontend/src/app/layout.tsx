import './globals.css';
import { ReactNode } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';


export const metadata = {
  title: 'treee',
  description: 'treee 홈페이지입니다.',
  openGraph: {
    type: 'website',
    url: 'https://www.treee.com/',
    title: 'treee',
    description: 'treee 홈페이지입니다.',
    images: [
      {
        url: 'https://www.yourwebsite.com/og-image.jpg',
        width: 800,
        height: 600,
        alt: 'treee 오픈 그래프 이미지',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'treee',
    description: 'treee 홈페이지입니다.',
    images: ['https://www.yourwebsite.com/twitter-image.jpg'],
  },
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ko">
      <body className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}