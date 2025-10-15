import MainLayout from '@/components/MainLayout';

export default function Home() {
  return (
    <MainLayout>
      <div className="max-w-6xl mx-auto">
        {/* Hero Section */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            Welcome to Dialektor
          </h1>
          <p className="text-lg text-gray-600">
            Explore how words are said and spelled across different dialects of the Albanian language
          </p>
        </div>

        {/* Content Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">🗣️</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Explore Dialects
            </h3>
            <p className="text-gray-600">
              Discover the rich variety of Albanian dialects from different regions
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">📖</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Word Comparisons
            </h3>
            <p className="text-gray-600">
              Compare how the same word is expressed in different Albanian dialects
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">🌍</span>
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Regional Variations
            </h3>
            <p className="text-gray-600">
              Learn about regional linguistic differences across Albania
            </p>
          </div>
        </div>

        {/* Stats Section */}
        <div className="mt-12 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-8 border border-blue-100">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            Why Dialektor?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">Comprehensive</div>
              <p className="text-gray-700">
                A complete database of dialectal variations
              </p>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">Educational</div>
              <p className="text-gray-700">
                Learn about the Albanian linguistic heritage
              </p>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">Interactive</div>
              <p className="text-gray-700">
                Explore and contribute to the collection
              </p>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

