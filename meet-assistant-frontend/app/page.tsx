import Image from 'next/image'
import Link from 'next/link'
import { ChevronDown, Globe } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Top banner */}
      <div className="bg-indigo-600 py-2 text-center text-sm text-white">
        <p>
          Read AI for Gmail released. Series B to deliver Copilot Everywhere.{' '}
          <Link href="#" className="underline">
            Learn more
          </Link>
        </p>
      </div>

      {/* Navigation */}
      <nav className="container mx-auto flex items-center justify-between py-4">
        <div className="flex items-center space-x-2">
          <div className="h-8 w-8 bg-indigo-600 rounded-lg"></div>
          <span className="text-xl font-bold">Read</span>
        </div>
        <div className="hidden md:flex space-x-4">
          <NavItem title="Meetings" hasDropdown />
          <NavItem title="Email" />
          <NavItem title="Messaging" />
          <NavItem title="Features" hasDropdown />
          <NavItem title="Pricing" hasDropdown />
          <NavItem title="About" hasDropdown />
        </div>
        <div className="flex items-center space-x-4">
          <Link href="#" className="text-indigo-600 hover:underline">
            Contact Sales
          </Link>
          <Link href="#" className="text-indigo-600 hover:underline">
            Login
          </Link>
          <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors">
            Try for free!
          </button>
          <button className="flex items-center space-x-1 text-gray-600">
            <Globe className="h-4 w-4" />
            <span>EN</span>
            <ChevronDown className="h-4 w-4" />
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto mt-16 grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
        <div>
          <h1 className="text-6xl font-bold mb-4">
            Meeting
            <br />
            <span className="text-gray-800">Copilot</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Read AI is an AI copilot for wherever you work, making your meetings, emails, and messages more productive with summaries, content discovery, and recommendations.
          </p>
          <div className="flex space-x-4 mb-8">
            <button className="bg-indigo-600 text-white px-6 py-3 rounded-md hover:bg-indigo-700 transition-colors">
              7-day free trial
            </button>
            <button className="border border-indigo-600 text-indigo-600 px-6 py-3 rounded-md hover:bg-indigo-50 transition-colors">
              Add to Chrome
            </button>
          </div>
          <p className="text-sm text-gray-500 mb-8">
            ✨ 5 free meetings per month! No software to install, no credit card required.
          </p>
          <div>
            <p className="text-sm text-gray-600 mb-2">Works with:</p>
            <div className="flex space-x-4">
              {['apple', 'google-meet', 'zoom', 'teams', 'gmail', 'outlook', 'google-calendar', 'hubspot', 'salesforce', 'slack', 'notion'].map((icon) => (
                <div key={icon} className="h-8 w-8 bg-gray-200 rounded-md"></div>
              ))}
            </div>
          </div>
        </div>
        <div className="bg-indigo-600 p-8 rounded-lg">
          <Image
            src="/placeholder.svg?height=400&width=500"
            alt="Read AI Interface"
            width={500}
            height={400}
            className="w-full h-auto"
          />
        </div>
      </section>

      {/* Copilot Everywhere Section */}
      <section className="container mx-auto mt-32 text-center">
        <h2 className="text-4xl font-bold mb-4">Copilot Everywhere</h2>
        <p className="text-xl text-gray-600 mb-16">
          75% of the Fortune 500 use Read AI to improve productivity by 20% (avg). Wherever you work, be more productive with Read AI.
        </p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {['Inbox AI', 'Live', 'In-Person', 'Workflow', 'Record and play', 'Upload audio', 'AI Meeting Notes', 'Action items and Share rec'].map((feature) => (
            <div key={feature} className="bg-gray-100 p-6 rounded-lg">
              <div className="h-12 w-12 bg-indigo-200 rounded-full mx-auto mb-4"></div>
              <p className="font-semibold">{feature}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

function NavItem({ title, hasDropdown = false }) {
  return (
    <div className="flex items-center space-x-1 cursor-pointer">
      <span>{title}</span>
      {hasDropdown && <ChevronDown className="h-4 w-4" />}
    </div>
  )
}