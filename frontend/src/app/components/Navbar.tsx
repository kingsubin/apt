'use client';

import { useState } from 'react';

export default function Navbar() {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    const toggleMobileMenu = () => {
        setIsMobileMenuOpen(!isMobileMenuOpen);
    };

    return (
        <nav className="fixed top-0 left-0 right-0 bg-white border-b border-gray-100 z-50">
            {/* 메인 네비게이션 컨테이너 */}
            <div className="max-w-7xl mx-auto px-6 h-[80px]">
                <div className="flex justify-between items-center h-full">
                    {/* 로고 영역 */}
                    <div className="flex items-center">
                        <a href="/" className="text-2xl font-bold text-gray-900">treee</a>
                    </div>

                    {/* 데스크톱 메뉴 */}
                    <div className="hidden md:flex items-center space-x-8">
                        <a href="/home" className="text-[17px] font-medium text-gray-900 hover:text-blue-600 transition-colors">매매</a>
                        <a href="/about" className="text-[17px] font-medium text-gray-900 hover:text-blue-600 transition-colors">전월세</a>
                    </div>

                    {/* 모바일 메뉴 버튼 */}
                    <div className="md:hidden">
                        <button
                            onClick={toggleMobileMenu}
                            className="text-gray-900 hover:text-blue-600 focus:outline-none"
                        >
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>

            {/* 모바일 메뉴 드롭다운 */}
            {isMobileMenuOpen && (
                <div className="md:hidden bg-white border-t border-gray-100 shadow-lg">
                    <div className="max-w-7xl mx-auto px-6 py-4 space-y-3">
                        <a href="/home" className="block text-[17px] font-medium text-gray-900 hover:text-blue-600 transition-colors">매매</a>
                        <a href="/about" className="block text-[17px] font-medium text-gray-900 hover:text-blue-600 transition-colors">전월세</a>
                    </div>
                </div>
            )}
        </nav>
    );
}