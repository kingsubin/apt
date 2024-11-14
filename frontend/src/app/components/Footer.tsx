export default function Footer() {
    return (
        <footer className="bg-white text-gray-800 py-8">
            <div className="container mx-auto flex flex-col md:flex-row justify-between items-start px-4">
                <div className="flex-1 mb-4 md:mb-0">
                    <h2 className="text-lg font-bold mb-2">Kindom</h2>
                    <p className="text-sm">부동산에 대한 모든 정보</p>
                </div>
                <div className="flex-1 mb-4 md:mb-0">
                    <h3 className="font-semibold mb-2">서비스</h3>
                    <ul className="space-y-2">
                        <li><a href="/about" className="hover:text-blue-500 text-sm">회사 소개</a></li>
                        <li><a href="/services" className="hover:text-blue-500 text-sm">서비스 안내</a></li>
                        <li><a href="/faq" className="hover:text-blue-500 text-sm">자주 묻는 질문</a></li>
                    </ul>
                </div>
                <div className="flex-1 mb-4 md:mb-0">
                    <h3 className="font-semibold mb-2">고객 지원</h3>
                    <ul className="space-y-2">
                        <li><a href="/contact" className="hover:text-blue-500 text-sm">고객센터</a></li>
                        <li><a href="/privacy" className="hover:text-blue-500 text-sm">개인정보 처리방침</a></li>
                        <li><a href="/terms" className="hover:text-blue-500 text-sm">이용 약관</a></li>
                    </ul>
                </div>
                <div className="flex-1">
                    <h3 className="font-semibold mb-2">소셜 미디어</h3> {/* 간격 추가 */}
                    <div className="flex flex-col space-y-2">
                        <a href="https://twitter.com" className="hover:text-blue-500 flex items-center">
                            <i className="fab fa-twitter mr-2"></i> {/* Twitter 아이콘 */}
                            <span className="text-sm">Twitter</span>
                        </a>
                        <a href="https://facebook.com" className="hover:text-blue-500 flex items-center">
                            <i className="fab fa-facebook mr-2"></i> {/* Facebook 아이콘 */}
                            <span className="text-sm">Facebook</span>
                        </a>
                        <a href="https://instagram.com" className="hover:text-blue-500 flex items-center">
                            <i className="fab fa-instagram mr-2"></i> {/* Instagram 아이콘 */}
                            <span className="text-sm">Instagram</span>
                        </a>
                    </div>
                </div>
            </div>
            <div className="text-center mt-4">
                <p className="text-sm">&copy; {new Date().getFullYear()} Kindom. All rights reserved.</p>
            </div>
        </footer>
    );
}