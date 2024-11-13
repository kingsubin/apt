export default function Footer() {
    return (
        <footer className="bg-gray-800 text-white py-4">
            <div className="container mx-auto flex flex-col md:flex-row justify-between items-center px-4">
                <div className="mb-2 md:mb-0">
                    <a href="/" className="text-xl font-bold">treee</a>
                </div>
                <div className="flex space-x-4">
                    <a href="/privacy" className="hover:text-gray-400">개인정보 보호</a>
                    <a href="/terms" className="hover:text-gray-400">이용 약관</a>
                    <a href="/contact" className="hover:text-gray-400">문의하기</a>
                </div>
                <div className="mt-2 md:mt-0">
                    <p className="text-sm">&copy; {new Date().getFullYear()} treee. 모든 권리 보유.</p>
                </div>
            </div>
        </footer>
    );
}