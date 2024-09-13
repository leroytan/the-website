import BurgerMenu from './components/BurgerMenu'
import LoginIcon from './components/LoginIcon'
import ReviewCarousel from './components/ReviewCarousel'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-100">
      <header className="bg-white shadow-md fixed top-0 left-0 right-0 z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <BurgerMenu />
          <h1 className="text-2xl font-bold text-blue-600">THE</h1>
          <LoginIcon />
        </div>
      </header>

      <main className="pt-16">
        <section className="py-20 bg-white">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-4xl font-extrabold mb-6 text-purple-700">Welcome to T.H.E.</h2>
            <p className="mb-8 text-lg leading-relaxed">
              This is a simple single-page website with a burger menu on the top left and a login logo on the top right. 
              Scroll down to explore more sections!
            </p>
            <div className="flex justify-center space-x-4">
              <button className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors duration-200">
                Request a tutor
              </button>
              <button className="bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors duration-200">
                Join Us
              </button>
            </div>
          </div>
        </section>

        <section className="py-20 bg-gray-100">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-8 text-blue-600">Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {['Responsive design', 'Interactive menu', 'Scrollable sections', 'Custom typography'].map((feature, index) => (
                <div key={index} className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-xl font-semibold mb-2">{feature}</h3>
                  <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="py-20 bg-blue-600 text-white">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-8">Why Join Us</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {['Flexible Hours', 'Competitive Pay', 'Professional Development'].map((reason, index) => (
                <div key={index} className="bg-blue-500 rounded-lg shadow-md p-6">
                  <h3 className="text-xl font-semibold mb-2">{reason}</h3>
                  <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="py-20 bg-purple-100">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-8 text-purple-700">Meet the Team</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {['John Doe', 'Jane Smith', 'Mike Johnson', 'Emily Brown'].map((member, index) => (
                <div key={index} className="bg-white rounded-lg shadow-md p-6 text-center">
                  <div className="w-24 h-24 bg-gray-300 rounded-full mx-auto mb-4"></div>
                  <h3 className="text-xl font-semibold mb-2">{member}</h3>
                  <p className="text-gray-600">Position</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="py-20 bg-gray-800 text-white">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-8">Programmes</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {['Math Tutoring', 'Science Courses', 'Language Classes', 'Test Preparation', 'Coding Bootcamps', 'Art Workshops'].map((programme, index) => (
                <div key={index} className="bg-gray-700 rounded-lg shadow-md p-6">
                  <h3 className="text-xl font-semibold mb-2">{programme}</h3>
                  <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="py-20 bg-white">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-8 text-blue-600">Reviews</h2>
            <ReviewCarousel />
          </div>
        </section>
      </main>

      <footer className="bg-gray-900 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p>&copy; 2024 My Website. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}