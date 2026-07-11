import { useState, useEffect, useRef, useCallback } from 'react'
import { useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Send, Scale, BookOpen, ChevronDown, Loader2, AlertCircle, Plus, Copy, Check, Trash2, MessageSquare } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import api from '../services/api'
import { v4 as uuidv4 } from 'uuid'
import toast from 'react-hot-toast'

const DOMAIN_COLORS = {
  Criminal: 'border-red-500/40 text-red-400 bg-red-500/10',
  Civil: 'border-blue-500/40 text-blue-400 bg-blue-500/10',
  Constitutional: 'border-purple-500/40 text-purple-400 bg-purple-500/10',
  Family: 'border-green-500/40 text-green-400 bg-green-500/10',
  Property: 'border-orange-500/40 text-orange-400 bg-orange-500/10',
  Labour: 'border-yellow-500/40 text-yellow-400 bg-yellow-500/10',
  Corporate: 'border-cyan-500/40 text-cyan-400 bg-cyan-500/10',
  Tax: 'border-emerald-500/40 text-emerald-400 bg-emerald-500/10',
  General: 'border-gray-500/40 text-gray-400 bg-gray-500/10',
}

const SUGGESTED = [
  { q: 'What is IPC Section 302?', icon: '⚖️' },
  { q: 'How to file for divorce?', icon: '👨‍👩‍👧' },
  { q: 'What are my fundamental rights?', icon: '🏛️' },
  { q: 'Can employer terminate without notice?', icon: '👷' },
  { q: 'How is GST calculated on services?', icon: '💰' },
  { q: 'What is domestic violence law in India?', icon: '🛡️' },
]

function CopyButton({ text }) {
  const [copied, setCopied] = useState(false)
  const handleCopy = () => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }
  return (
    <button onClick={handleCopy} className="p-1.5 rounded-md text-gray-600 hover:text-gray-400 hover:bg-dark-600 transition-all" title="Copy response">
      {copied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
    </button>
  )
}

function SourcePanel({ sources, isOpen, onToggle }) {
  if (!sources || sources.length === 0) return null
  return (
    <div className="mt-2">
      <button onClick={onToggle} className="flex items-center gap-1.5 text-xs text-gold-400/80 hover:text-gold-400 transition-colors py-1">
        <BookOpen className="w-3.5 h-3.5" />
        <span>{sources.length} legal source{sources.length > 1 ? 's' : ''} cited</span>
        <ChevronDown className={`w-3.5 h-3.5 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
      </button>
      {isOpen && (
        <div className="mt-2 space-y-2 animate-fade-in">
          {sources.map((src, i) => (
            <div key={i} className="bg-dark-700/60 border border-dark-500/50 rounded-lg p-3">
              <div className="flex items-start justify-between gap-2 mb-1.5">
                <span className="font-medium text-gold-400 text-xs leading-tight">{src.title}</span>
                <span className="text-xs text-gray-600 whitespace-nowrap flex-shrink-0 bg-dark-600 px-1.5 py-0.5 rounded">{src.relevance}%</span>
              </div>
              <p className="text-gray-500 text-xs leading-relaxed">{src.snippet}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function AssistantMessage({ msg }) {
  const [sourcesOpen, setSourcesOpen] = useState(false)
  return (
    <div className="flex gap-3 animate-slide-up max-w-4xl">
      <div className="w-8 h-8 bg-gold-500/20 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
        <Scale className="w-4 h-4 text-gold-500" />
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xs font-semibold text-gold-400">LAWAI</span>
          {msg.domain && (
            <span className={`domain-badge text-xs ${DOMAIN_COLORS[msg.domain] || DOMAIN_COLORS.General}`}>
              {msg.domain}
            </span>
          )}
          <div className="ml-auto">
            <CopyButton text={msg.content} />
          </div>
        </div>
        <div className="card prose prose-invert prose-sm max-w-none
          prose-headings:text-gold-400 prose-headings:font-semibold prose-headings:mt-4 prose-headings:mb-2
          prose-h2:text-base prose-h3:text-sm
          prose-strong:text-gray-200 prose-strong:font-semibold
          prose-ul:my-2 prose-li:my-0.5
          prose-p:text-gray-300 prose-p:leading-relaxed
          prose-code:text-gold-300 prose-code:bg-dark-700 prose-code:px-1 prose-code:rounded
          border-gold-500/10">
          <ReactMarkdown>{msg.content}</ReactMarkdown>
        </div>
        <SourcePanel sources={msg.sources} isOpen={sourcesOpen} onToggle={() => setSourcesOpen(!sourcesOpen)} />
      </div>
    </div>
  )
}

export default function ChatPage() {
  const { user } = useAuth()
  const location = useLocation()
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionId] = useState(uuidv4())
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  const hasAutoSent = useRef(false)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  useEffect(() => {
    if (location.state?.initialQuery && !hasAutoSent.current) {
      hasAutoSent.current = true
      sendMessage(location.state.initialQuery)
    }
  }, [])

  const sendMessage = useCallback(async (queryOverride) => {
    const query = (queryOverride !== undefined ? queryOverride : input).trim()
    if (!query || loading) return
    setInput('')
    setLoading(true)

    setMessages(prev => [...prev, { role: 'user', content: query, id: Date.now() }])

    try {
      const token = localStorage.getItem('lawai_token')
      const headers = token ? { Authorization: `Bearer ${token}` } : {}
      const res = await api.post('/api/chat/ask', { query, session_id: sessionId }, { headers })
      const { answer, domain, sources } = res.data
      setMessages(prev => [...prev, { role: 'assistant', content: answer, domain, sources, id: Date.now() + 1 }])
    } catch (err) {
      const errMsg = err.response?.data?.error || 'Connection error. Ensure backend is running on port 5000.'
      toast.error('Failed to get response')
      setMessages(prev => [...prev, { role: 'error', content: errMsg, id: Date.now() + 1 }])
    } finally {
      setLoading(false)
      setTimeout(() => inputRef.current?.focus(), 100)
    }
  }, [input, loading, sessionId])

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage() }
  }

  const clearChat = () => {
    setMessages([])
    toast.success('Chat cleared')
  }

  const isEmpty = messages.length === 0

  return (
    <div className="flex h-screen pt-16 bg-dark-900">
      {/* Sidebar */}
      <aside className="hidden lg:flex w-60 flex-col border-r border-dark-600/70 bg-dark-800/30 p-3 gap-3">
        <button onClick={clearChat} className="flex items-center gap-2 w-full px-3 py-2.5 rounded-lg border border-dark-500 text-gray-400 hover:text-gold-400 hover:border-gold-500/40 text-sm font-medium transition-all">
          <Plus className="w-4 h-4" />New Chat
        </button>
        
        <div className="text-xs text-gray-600 uppercase tracking-wider px-1 pt-1">Quick Ask</div>
        <div className="flex-1 space-y-0.5 overflow-y-auto">
          {SUGGESTED.map(({ q, icon }) => (
            <button key={q} onClick={() => sendMessage(q)} disabled={loading}
              className="w-full text-left flex items-start gap-2 text-xs text-gray-500 hover:text-gray-300 hover:bg-dark-700 px-2.5 py-2 rounded-lg transition-all">
              <span className="text-base flex-shrink-0">{icon}</span>
              <span className="leading-tight">{q}</span>
            </button>
          ))}
        </div>
        
        {messages.length > 0 && (
          <button onClick={clearChat} className="flex items-center gap-2 text-xs text-gray-600 hover:text-red-400 px-2 py-1.5 rounded-lg hover:bg-red-500/10 transition-all">
            <Trash2 className="w-3.5 h-3.5" />Clear chat
          </button>
        )}
        
        <div className="text-xs text-gray-700 text-center pb-1">
          {user ? `● ${user.name?.split(' ')[0]}` : '○ Guest mode'}
        </div>
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 md:px-8 py-6 space-y-6">
          {isEmpty && (
            <div className="flex flex-col items-center justify-center h-full text-center py-16 animate-fade-in">
              <div className="w-24 h-24 bg-gradient-to-br from-gold-500/20 to-gold-600/5 rounded-3xl flex items-center justify-center mb-6 border border-gold-500/20">
                <Scale className="w-12 h-12 text-gold-500" />
              </div>
              <h2 className="text-3xl font-bold font-serif mb-3">Ask LAWAI</h2>
              <p className="text-gray-500 max-w-md mb-10 text-sm leading-relaxed">
                Your AI legal companion for Indian law — IPC, constitutional rights, family law, property, labour, corporate, and tax law.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-lg w-full">
                {SUGGESTED.slice(0, 4).map(({ q, icon }) => (
                  <button key={q} onClick={() => sendMessage(q)}
                    className="card text-left flex items-center gap-3 py-3 px-4 hover:-translate-y-0.5 transition-all text-sm group">
                    <span className="text-xl">{icon}</span>
                    <span className="text-gray-400 group-hover:text-gray-200 transition-colors">{q}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg) => (
            <div key={msg.id}>
              {msg.role === 'user' && (
                <div className="flex justify-end animate-slide-up">
                  <div className="max-w-2xl bg-gradient-to-br from-gold-500/20 to-gold-600/10 border border-gold-500/20 rounded-2xl rounded-tr-sm px-4 py-3 text-gray-200 text-sm leading-relaxed">
                    {msg.content}
                  </div>
                </div>
              )}
              {msg.role === 'assistant' && <AssistantMessage msg={msg} />}
              {msg.role === 'error' && (
                <div className="flex gap-3 animate-fade-in">
                  <div className="w-8 h-8 bg-red-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                    <AlertCircle className="w-4 h-4 text-red-400" />
                  </div>
                  <div className="card border-red-500/20 text-sm text-red-300/80 py-3">{msg.content}</div>
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex gap-3 animate-fade-in">
              <div className="w-8 h-8 bg-gold-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                <Scale className="w-4 h-4 text-gold-500" />
              </div>
              <div className="card flex items-center gap-3 py-3 px-4">
                <div className="flex gap-1.5">
                  <div className="w-2 h-2 bg-gold-500 rounded-full animate-bounce" style={{animationDelay:'0ms'}} />
                  <div className="w-2 h-2 bg-gold-500 rounded-full animate-bounce" style={{animationDelay:'150ms'}} />
                  <div className="w-2 h-2 bg-gold-500 rounded-full animate-bounce" style={{animationDelay:'300ms'}} />
                </div>
                <span className="text-sm text-gray-500">Searching legal corpus...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="border-t border-dark-600/70 bg-dark-800/30 px-4 md:px-8 py-4">
          <div className="max-w-4xl mx-auto">
            <div className="flex gap-3 items-end">
              <div className="flex-1 relative">
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={handleKey}
                  placeholder="Ask about any aspect of Indian law... (Enter to send)"
                  rows={1}
                  disabled={loading}
                  className="input-field w-full resize-none py-3 pr-16 text-sm leading-relaxed disabled:opacity-60"
                  style={{ minHeight: '48px', maxHeight: '160px', overflowY: 'auto' }}
                  onInput={e => { e.target.style.height = 'auto'; e.target.style.height = Math.min(e.target.scrollHeight, 160) + 'px' }}
                />
                <span className="absolute right-3 bottom-3 text-xs text-gray-700">{input.length}/500</span>
              </div>
              <button
                onClick={() => sendMessage()}
                disabled={!input.trim() || loading}
                className="flex-shrink-0 w-12 h-12 bg-gold-500 hover:bg-gold-400 disabled:bg-dark-600 disabled:cursor-not-allowed text-dark-900 disabled:text-gray-600 rounded-xl flex items-center justify-center transition-all hover:shadow-lg hover:shadow-gold-500/20 active:scale-95">
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
              </button>
            </div>
            <p className="text-xs text-gray-700 text-center mt-2">
              LAWAI provides general legal information only. Consult a qualified lawyer for specific legal advice.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
