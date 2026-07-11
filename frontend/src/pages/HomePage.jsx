import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Scale, MessageSquare, BookOpen, Users, Shield, Zap, ArrowRight, Search, ChevronRight, Database, Brain, FileText } from 'lucide-react'

const DOMAINS = [
  { icon: '⚖️', name: 'Criminal Law', desc: 'IPC, CrPC, bail, FIR', color: 'text-red-400' },
  { icon: '📜', name: 'Civil Law', desc: 'Contracts & disputes', color: 'text-blue-400' },
  { icon: '🏛️', name: 'Constitutional', desc: 'Rights & PIL', color: 'text-purple-400' },
  { icon: '👨‍👩‍👧', name: 'Family Law', desc: 'Marriage & custody', color: 'text-green-400' },
  { icon: '🏠', name: 'Property Law', desc: 'Land & registry', color: 'text-orange-400' },
  { icon: '👷', name: 'Labour Law', desc: 'Employment rights', color: 'text-yellow-400' },
  { icon: '🏢', name: 'Corporate Law', desc: 'Company & compliance', color: 'text-cyan-400' },
  { icon: '💰', name: 'Tax Law', desc: 'GST, Income Tax', color: 'text-emerald-400' },
]

const FEATURES = [
  { icon: Brain, title: 'RAG-Powered Intelligence', desc: 'Retrieval-Augmented Generation retrieves the most relevant IPC sections, constitutional articles, and case law before generating your answer.' },
  { icon: FileText, title: 'Provenance-Based Citations', desc: 'Every answer includes exact section numbers, article references, and landmark case citations so you can verify the information.' },
  { icon: Database, title: 'Domain-Aware Routing', desc: 'Automatically routes your query to the right legal domain — Criminal, Civil, Constitutional, Family, Property, Labour, Corporate, or Tax.' },
  { icon: Users, title: 'Expert Connect', desc: 'Connect with verified Indian lawyers for personalized legal advice and professional representation when AI isn\'t enough.' },
]

const HOW_IT_WORKS = [
  { step: '01', title: 'Ask Your Question', desc: 'Type your legal query in plain language — no legal jargon needed.', icon: MessageSquare },
  { step: '02', title: 'AI Searches Corpus', desc: 'Our RAG system retrieves relevant IPC sections, articles, and case law.', icon: Database },
  { step: '03', title: 'Get Cited Answer', desc: 'Receive a structured answer with exact legal citations and sources.', icon: FileText },
]

const SAMPLE_QUERIES = [
  'What is IPC Section 302?',
  'Grounds for divorce in India',
  'What are my fundamental rights?',
  'How to file a consumer complaint?',
]

export default function HomePage() {
  const [query, setQuery] = useState('')
  const [activeQuery, setActiveQuery] = useState(0)
  const navigate = useNavigate()

  useEffect(() => {
    const timer = setInterval(() => setActiveQuery(p => (p + 1) % SAMPLE_QUERIES.length), 3000)
    return () => clearInterval(timer)
  }, [])

  const handleAsk = (e) => {
    e.preventDefault()
    if (query.trim()) navigate('/chat', { state: { initialQuery: query } })
  }

  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="relative pt-28 pb-24 px-4 overflow-hidden">
        {/* Background blobs */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-gold-500/3 rounded-full blur-3xl transform translate-x-1/3 -translate-y-1/4" />
          <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-purple-500/3 rounded-full blur-3xl transform -translate-x-1/3 translate-y-1/4" />
          <div className="absolute top-1/2 left-1/2 w-[400px] h-[400px] bg-blue-500/3 rounded-full blur-3xl transform -translate-x-1/2 -translate-y-1/2" />
        </div>
        
        <div className="relative max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 glass px-4 py-2 rounded-full text-sm text-gold-400 mb-8 border border-gold-500/20 animate-fade-in">
            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            <span>AI-Powered Indian Legal Assistant — 100% Free</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6 font-serif leading-tight animate-fade-in">
            Legal Clarity at
            <br />
            <span className="gradient-text">Your Fingertips</span>
          </h1>
          
          <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed">
            Ask any question on Indian law. Get instant, cited answers backed by IPC, constitutional articles, and landmark Supreme Court judgments.
          </p>
          
          <form onSubmit={handleAsk} className="flex flex-col sm:flex-row gap-3 max-w-2xl mx-auto mb-6">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="text"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder={SAMPLE_QUERIES[activeQuery]}
                className="input-field pl-12 h-14 text-base transition-all"
              />
            </div>
            <button type="submit" className="btn-gold flex items-center justify-center gap-2 h-14 sm:w-auto w-full whitespace-nowrap">
              Ask LAWAI <ArrowRight className="w-4 h-4" />
            </button>
          </form>
          
          <div className="flex flex-wrap justify-center gap-2 text-sm">
            {SAMPLE_QUERIES.map(s => (
              <button key={s} onClick={() => setQuery(s)}
                className="glass px-3 py-1.5 rounded-full text-gray-500 hover:text-gold-400 hover:border-gold-500/30 transition-all text-xs border border-transparent">
                {s}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-10 border-y border-dark-600/50 bg-dark-800/20">
        <div className="max-w-5xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          {[
            { num: '35+', label: 'Legal Documents', sub: 'IPC, Constitutional, Case Law' },
            { num: '8', label: 'Legal Domains', sub: 'Complete coverage' },
            { num: '100%', label: 'Free Forever', sub: 'No credit card' },
            { num: '6+', label: 'Expert Lawyers', sub: 'Book consultations' },
          ].map(stat => (
            <div key={stat.label} className="py-2">
              <div className="text-3xl font-bold gradient-text mb-1">{stat.num}</div>
              <div className="text-gray-300 text-sm font-medium">{stat.label}</div>
              <div className="text-gray-600 text-xs mt-0.5">{stat.sub}</div>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="py-20 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl md:text-4xl font-bold font-serif mb-3">How <span className="gradient-text">LAWAI</span> Works</h2>
            <p className="text-gray-500">Powered by Retrieval-Augmented Generation (RAG)</p>
          </div>
          <div className="grid md:grid-cols-3 gap-6 relative">
            <div className="hidden md:block absolute top-8 left-1/4 right-1/4 h-px bg-gradient-to-r from-gold-500/20 via-gold-500/50 to-gold-500/20" />
            {HOW_IT_WORKS.map(({ step, title, desc, icon: Icon }, i) => (
              <div key={step} className="card text-center relative">
                <div className="w-14 h-14 mx-auto bg-gold-500/10 rounded-2xl flex items-center justify-center mb-4 border border-gold-500/20">
                  <Icon className="w-7 h-7 text-gold-500" />
                </div>
                <div className="text-xs font-bold text-gold-500/50 tracking-widest mb-2">STEP {step}</div>
                <h3 className="font-semibold text-white mb-2">{title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-4 bg-dark-800/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl md:text-4xl font-bold font-serif mb-3">Built for <span className="gradient-text">Indian Law</span></h2>
            <p className="text-gray-500 max-w-xl mx-auto">Purpose-built for the Indian legal system with cutting-edge AI</p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-5">
            {FEATURES.map(({ icon: Icon, title, desc }) => (
              <div key={title} className="card group hover:-translate-y-1.5 transition-all duration-300 cursor-default">
                <div className="w-12 h-12 bg-gold-500/10 group-hover:bg-gold-500/20 rounded-xl flex items-center justify-center mb-4 transition-colors">
                  <Icon className="w-6 h-6 text-gold-500" />
                </div>
                <h3 className="font-semibold text-white mb-2 text-sm">{title}</h3>
                <p className="text-gray-500 text-xs leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Domains */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl md:text-4xl font-bold font-serif mb-3">8 Legal <span className="gradient-text">Domains</span></h2>
            <p className="text-gray-500">Comprehensive coverage of Indian law</p>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {DOMAINS.map(({ icon, name, desc, color }) => (
              <Link key={name} to="/chat"
                className="card text-center hover:-translate-y-1.5 transition-all duration-300 group">
                <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">{icon}</div>
                <h3 className={`font-semibold text-sm mb-1 ${color}`}>{name}</h3>
                <p className="text-gray-600 text-xs">{desc}</p>
                <div className={`mt-3 text-xs ${color} opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-1`}>
                  Ask now <ChevronRight className="w-3 h-3" />
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-4">
        <div className="max-w-3xl mx-auto">
          <div className="card border-gold-500/20 bg-gradient-to-br from-gold-500/5 to-transparent text-center py-12">
            <Scale className="w-12 h-12 text-gold-500 mx-auto mb-6" />
            <h2 className="text-3xl md:text-4xl font-bold font-serif mb-4">
              Ready for <span className="gradient-text">Legal Clarity</span>?
            </h2>
            <p className="text-gray-400 mb-8 max-w-md mx-auto">Join thousands using LAWAI for quick, accurate, cited legal information.</p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/chat" className="btn-gold flex items-center justify-center gap-2">
                <MessageSquare className="w-5 h-5" />Start Chatting Free
              </Link>
              <Link to="/experts" className="btn-outline flex items-center justify-center gap-2">
                <Users className="w-5 h-5" />Talk to a Lawyer
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-dark-600/50 py-10 px-4">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Scale className="w-5 h-5 text-gold-500" />
            <span className="text-gold-400 font-bold font-serif">LAWAI</span>
            <span className="text-gray-600 text-sm">— AI Legal Assistant</span>
          </div>
          <div className="flex gap-6 text-sm text-gray-600">
            <Link to="/chat" className="hover:text-gray-400 transition-colors">Chat</Link>
            <Link to="/experts" className="hover:text-gray-400 transition-colors">Experts</Link>
            <Link to="/register" className="hover:text-gray-400 transition-colors">Register</Link>
          </div>
          <p className="text-gray-700 text-xs text-center">Not a substitute for professional legal advice. © 2024 LAWAI</p>
        </div>
      </footer>
    </div>
  )
}
