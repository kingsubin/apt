import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Kindom",
  description: "부동산 실거래가 데이터 제공",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className={inter.className}>
        {/* 전체 레이아웃 유지 */}
        <div className="max-w-7xl mx-auto px-6">
          <Navbar />
          {/* Navbar 높이(80px)만큼 상단 여백 추가 */}
          <main className="pt-[80px] min-h-screen">
            {/* 최대 너비 제한과 중앙 정렬을 위한 컨테이너 */}
            <div className="max-w-7xl mx-auto">
              {children}
            </div>
          </main>
          <Footer />
        </div>
      </body>
    </html >
  );
}