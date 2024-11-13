'use client';

import { useState } from 'react';

export default function Navbar() {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    const toggleMobileMenu = () => {
        setIsMobileMenuOpen(!isMobileMenuOpen);
    };

    return (
        <nav className="bg-white border-b border-gray-200 px-4 py-3">
            <div className="flex justify-between items-center">
                <div className="flex items-center">
                    <a href="/" className="text-xl font-bold text-gray-800">treee</a>
                </div>
                <div className="hidden md:flex space-x-4">
                    <a href="/home" className="text-gray-600 hover:text-gray-800">홈</a>
                    <a href="/about" className="text-gray-600 hover:text-gray-800">소개</a>
                    <a href="/contact" className="text-gray-600 hover:text-gray-800">문의</a>
                </div>
                <div className="md:hidden">
                    <button
                        onClick={toggleMobileMenu}
                        className="text-gray-600 hover:text-gray-800 focus:outline-none"
                    >
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>
            </div>
            {isMobileMenuOpen && (
                <div className="md:hidden mt-2">
                    <a href="/home" className="block px-2 py-1 text-gray-600 hover:text-gray-800">홈</a>
                    <a href="/about" className="block px-2 py-1 text-gray-600 hover:text-gray-800">소개</a>
                    <a href="/contact" className="block px-2 py-1 text-gray-600 hover:text-gray-800">문의</a>
                </div>
            )}
        </nav>
    );
} 