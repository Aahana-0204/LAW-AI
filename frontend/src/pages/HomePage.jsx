import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import {
  ArrowRight,
  BookOpen,
  MessageSquare,
  Scale,
  Search,
  Shield,
  Users,
  Zap,
} from 'lucide-react'

const DOMAINS = [
  { icon: '⚖️', name: 'Criminal Law', desc: 'IPC sections, bail, FIR', color: 'red' },
  { icon: '📜', name: 'Civil Law', desc: 'Contracts & disputes', color: 'blue' },
  { icon: '🏛️', name: 'Constitutional', desc: 'Rights & PIL', color: 'purple' },
  { icon: '👨‍👩‍👧', name: 'Family Law', desc: 'Marriage & custody', color: 'green' },
  { icon: '🏠', name: 'Property Law', desc: 'Land & registry', color: 'orange' },
  { icon: '👷', name: 'Labour Law', desc: 'Employment rights', color: 'yellow' },
  { icon: '🏢', name: 'Corporate Law', desc: 'Company & compliance', color: 'cyan' },
  { icon: '💰', name: 'Tax Law', desc: 'GST, Income Tax', color: 'emerald' },
]

const FEATURES = [
  {
    icon: Zap,
    title: 'RAG-Powered Answers',
    desc: 'Retrieval-Augmented Generation on curated IPC sections, constitutional articles, and landmark case law for accurate, grounded responses.',
  },
  {
    icon: BookOpen,
    title: 'Source Attribution',
    desc: 'Every answer includes citations — specific sections, articles, and case names so you know exactly where the information comes from.',
  },
  {
    icon: Shield,
    title: 'Domain-Aware Routing',
    desc: 'Automatically detects whether your query is Criminal, Civil, Constitutional, Family, Property, Labour, Corporate, or Tax law.',
  },
  {
    icon: Users,
    title: 'Expert Connect',
    desc: 'Connect with verified legal professionals for complex matters requiring personalized legal advice and representation.',
  },
]

export default function HomePage() {
  const [query, setQuery] = useState('')
  const navigate = useNavigate()

  const handleAsk = (e) => {
    e.preventDefault()
    if (query.trim()) {
      navigate('/chat', { state: { initialQuery: query } })
    }
  }

  return (
    <div className="min-h-screen">
      <section className="relative overflow-hidden px-4 pb-24 pt-32">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -right-40 -top-40 h-96 w-96 rounded-full bg-gold-500/5 blur-3xl" />
          <div className="absolute -bottom-40 -left-40 h-96 w-96 rounded-full bg-purple-500/5 blur-3xl" />
        </div>

        <div className="relative mx-auto max-w-4xl text-center">
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-gold-500/20 px-4 py-2 text-sm text-gold-400 glass">
            <Scale className="h-4 w-4" />
            <span>AI-Powered Indian Legal Assistant</span>
          </div>

          <h1 className="mb-6 font-serif text-5xl font-bold leading-tight md:text-7xl">
            Your <span className="gradient-text">AI-Powered Legal</span>
            <br />
            Companion
          </h1>

          <p className="mx-auto mb-10 max-w-2xl text-xl leading-relaxed text-gray-400">
            Get instant, accurate answers on Indian law — IPC sections, constitutional
            rights, case law, and more. Powered by RAG AI with source citations.
          </p>

          <form onSubmit={handleAsk} className="mx-auto mb-8 flex max-w-2xl gap-3">
            <div className="relative flex-1">
              <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-500" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask about IPC 302, bail conditions, divorce grounds..."
                className="input-field h-14 pl-12 text-base"
              />
            </div>
            <button type="submit" className="btn-gold flex h-14 items-center gap-2 whitespace-nowrap">
              Ask LAWAI <ArrowRight className="h-4 w-4" />
            </button>
          </form>

          <div className="flex flex-wrap justify-center gap-3 text-sm text-gray-500">
            {[
              'What is IPC Section 302?',
              'Grounds for divorce in India',
              'What are my fundamental rights?',
            ].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => {
                  setQuery(suggestion)
                }}
                className="rounded-full px-3 py-1.5 text-xs transition-all hover:border-gold-500/30 hover:text-gold-400 glass"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      </section>

      <section className="border-y border-dark-600 px-4 py-12">
        <div className="mx-auto grid max-w-4xl grid-cols-2 gap-8 text-center md:grid-cols-4">
          {[
            { num: '10K+', label: 'Legal Queries' },
            { num: '30+', label: 'IPC Sections' },
            { num: '8', label: 'Legal Domains' },
            { num: '6+', label: 'Expert Lawyers' },
          ].map((stat) => (
            <div key={stat.label}>
              <div className="mb-1 text-3xl font-bold gradient-text">{stat.num}</div>
              <div className="text-sm text-gray-500">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      <section className="px-4 py-20">
        <div className="mx-auto max-w-6xl">
          <div className="mb-12 text-center">
            <h2 className="mb-4 font-serif text-3xl font-bold md:text-4xl">
              Why Choose <span className="gradient-text">LAWAI</span>?
            </h2>
            <p className="mx-auto max-w-xl text-gray-400">
              Built specifically for the Indian legal system with elegant design and
              grounded AI.
            </p>
          </div>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {FEATURES.map(({ icon: Icon, title, desc }) => (
              <div key={title} className="card transition-transform hover:-translate-y-1">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-gold-500/10">
                  <Icon className="h-6 w-6 text-gold-500" />
                </div>
                <h3 className="mb-2 font-semibold text-white">{title}</h3>
                <p className="text-sm leading-relaxed text-gray-500">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="bg-dark-800/50 px-4 py-20">
        <div className="mx-auto max-w-6xl">
          <div className="mb-12 text-center">
            <h2 className="mb-4 font-serif text-3xl font-bold md:text-4xl">
              8 Legal <span className="gradient-text">Domains</span>
            </h2>
            <p className="text-gray-400">Comprehensive coverage across Indian law.</p>
          </div>
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            {DOMAINS.map(({ icon, name, desc }) => (
              <Link
                key={name}
                to="/chat"
                className="card cursor-pointer text-center transition-transform hover:-translate-y-1"
              >
                <div className="mb-3 text-4xl">{icon}</div>
                <h3 className="mb-1 text-sm font-semibold text-white">{name}</h3>
                <p className="text-xs text-gray-500">{desc}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="px-4 py-20">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="mb-4 font-serif text-3xl font-bold md:text-4xl">
            Ready to Get <span className="gradient-text">Legal Clarity</span>?
          </h2>
          <p className="mb-8 text-gray-400">
            Join thousands using LAWAI for fast, grounded legal information.
          </p>
          <div className="flex flex-col justify-center gap-4 sm:flex-row">
            <Link to="/chat" className="btn-gold flex items-center justify-center gap-2">
              <MessageSquare className="h-5 w-5" />
              Start Chatting Free
            </Link>
            <Link to="/experts" className="btn-outline flex items-center justify-center gap-2">
              <Users className="h-5 w-5" />
              Talk to an Expert
            </Link>
          </div>
        </div>
      </section>

      <footer className="border-t border-dark-600 px-4 py-8 text-center text-sm text-gray-600">
        <div className="mb-2 flex items-center justify-center gap-2">
          <Scale className="h-4 w-4 text-gold-500" />
          <span className="font-semibold text-gold-500">LAWAI</span>
        </div>
        <p>AI legal guidance for Indian law. Not a substitute for professional advice.</p>
      </footer>
    </div>
  )
}
