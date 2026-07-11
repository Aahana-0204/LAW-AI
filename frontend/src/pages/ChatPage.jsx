import { useEffect, useMemo, useRef, useState } from 'react'
import { useLocation } from 'react-router-dom'
import {
  AlertCircle,
  BookOpen,
  ChevronRight,
  Loader2,
  Menu,
  MessageSquare,
  PanelRight,
  Plus,
  Scale,
  Send,
  X,
} from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { v4 as uuidv4 } from 'uuid'
import toast from 'react-hot-toast'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'

const DOMAIN_COLORS = {
  Criminal: 'border-red-500/40 bg-red-500/10 text-red-400',
  Civil: 'border-blue-500/40 bg-blue-500/10 text-blue-400',
  Constitutional: 'border-purple-500/40 bg-purple-500/10 text-purple-400',
  Family: 'border-green-500/40 bg-green-500/10 text-green-400',
  Property: 'border-orange-500/40 bg-orange-500/10 text-orange-400',
  Labour: 'border-yellow-500/40 bg-yellow-500/10 text-yellow-400',
  Corporate: 'border-cyan-500/40 bg-cyan-500/10 text-cyan-400',
  Tax: 'border-emerald-500/40 bg-emerald-500/10 text-emerald-400',
  General: 'border-gray-500/40 bg-gray-500/10 text-gray-400',
}

const SUGGESTED_QUERIES = [
  'What is IPC Section 302?',
  'How to file for divorce?',
  'What are my fundamental rights?',
  'Can employer terminate without notice?',
  'How is GST calculated?',
  'What is domestic violence law?',
]

export default function ChatPage() {
  const { user } = useAuth()
  const location = useLocation()
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  const hasAutoSent = useRef(false)
  const [messages, setMessages] = useState([])
  const [sessions, setSessions] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState(uuidv4())
  const [showSources, setShowSources] = useState(null)
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false)
  const [sourceDrawerOpen, setSourceDrawerOpen] = useState(true)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    if (user) {
      fetchSessions()
    } else {
      setSessions([])
    }
  }, [user])

  useEffect(() => {
    if (location.state?.initialQuery && !hasAutoSent.current) {
      hasAutoSent.current = true
      setInput(location.state.initialQuery)
      sendMessage(location.state.initialQuery)
    }
  }, [location.state])

  const activeSources = useMemo(
    () => messages.find((msg) => msg.id === showSources)?.sources || [],
    [messages, showSources],
  )

  const fetchSessions = async () => {
    try {
      const res = await api.get('/api/chat/sessions')
      setSessions(res.data.sessions || [])
    } catch {
      setSessions([])
    }
  }

  const loadSession = async (selectedSessionId) => {
    try {
      const res = await api.get(`/api/chat/history/${selectedSessionId}`)
      const normalized = (res.data.messages || []).map((msg, index) => ({
        ...msg,
        id: `${selectedSessionId}-${index}-${msg._id || index}`,
      }))
      setSessionId(selectedSessionId)
      setMessages(normalized)
      setMobileSidebarOpen(false)
      const latestWithSources = [...normalized].reverse().find((msg) => msg.sources?.length)
      setShowSources(latestWithSources?.id || null)
    } catch {
      toast.error('Failed to load chat history')
    }
  }

  const startNewChat = () => {
    setSessionId(uuidv4())
    setMessages([])
    setInput('')
    setShowSources(null)
    setMobileSidebarOpen(false)
    inputRef.current?.focus()
  }

  const sendMessage = async (queryOverride) => {
    const query = (queryOverride || input).trim()
    if (!query || loading) return

    setInput('')
    setLoading(true)

    const userId = `user-${Date.now()}`
    const userMsg = { role: 'user', content: query, id: userId }
    setMessages((prev) => [...prev, userMsg])

    try {
      const token = localStorage.getItem('lawai_token')
      const headers = token ? { Authorization: `Bearer ${token}` } : {}
      const res = await api.post(
        '/api/chat/ask',
        { query, session_id: sessionId },
        { headers },
      )

      const { answer, domain, sources, session_id: returnedSessionId } = res.data
      const assistantId = `assistant-${Date.now()}`
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: answer, domain, sources, id: assistantId },
      ])
      setSessionId(returnedSessionId || sessionId)
      if (sources?.length > 0) {
        setShowSources(assistantId)
        setSourceDrawerOpen(true)
      }
      if (user) {
        fetchSessions()
      }
    } catch (err) {
      toast.error('Failed to get response. Check backend connection.')
      setMessages((prev) => [
        ...prev,
        {
          role: 'error',
          content: 'Connection error. Please ensure the backend is running.',
          id: `error-${Date.now()}`,
        },
      ])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="flex h-screen pt-16">
      {mobileSidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 lg:hidden"
          onClick={() => setMobileSidebarOpen(false)}
        />
      )}

      <aside
        className={`fixed left-0 top-16 z-50 flex h-[calc(100vh-4rem)] w-72 flex-col border-r border-dark-600 bg-dark-800/95 p-4 transition-transform lg:static lg:z-auto lg:w-72 lg:translate-x-0 lg:bg-dark-800/50 ${
          mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="mb-4 flex items-center justify-between lg:hidden">
          <span className="text-sm font-semibold text-gray-300">Chat Sessions</span>
          <button
            onClick={() => setMobileSidebarOpen(false)}
            className="rounded-lg p-2 text-gray-400 hover:bg-dark-700 hover:text-gold-400"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <button
          onClick={startNewChat}
          className="btn-outline mb-4 flex w-full items-center justify-center gap-2 py-2 text-sm"
        >
          <Plus className="h-4 w-4" />
          New Chat
        </button>

        <div className="mb-3 px-1 text-xs font-medium uppercase tracking-wider text-gray-600">
          {user ? 'Recent Sessions' : 'Suggested Topics'}
        </div>

        <div className="space-y-2 overflow-y-auto">
          {user
            ? sessions.map((session) => (
                <button
                  key={session._id}
                  onClick={() => loadSession(session._id)}
                  className={`w-full rounded-xl border p-3 text-left transition-all ${
                    sessionId === session._id
                      ? 'border-gold-500/40 bg-gold-500/10'
                      : 'border-dark-600 bg-dark-700/50 hover:border-gold-500/20 hover:bg-dark-700'
                  }`}
                >
                  <div className="mb-1 flex items-center gap-2">
                    <MessageSquare className="h-4 w-4 text-gold-500" />
                    <span className="truncate text-sm font-medium text-gray-200">
                      {session.domain || 'General'}
                    </span>
                  </div>
                  <p className="line-clamp-2 text-xs text-gray-500">
                    {session.last_msg || 'New conversation'}
                  </p>
                </button>
              ))
            : SUGGESTED_QUERIES.map((query) => (
                <button
                  key={query}
                  onClick={() => {
                    setInput(query)
                    setMobileSidebarOpen(false)
                    inputRef.current?.focus()
                  }}
                  className="w-full truncate rounded-lg px-3 py-2 text-left text-sm text-gray-400 transition-all hover:bg-dark-700 hover:text-gold-400"
                >
                  {query}
                </button>
              ))}
        </div>

        <div className="mt-auto pt-4 text-center text-xs text-gray-600">
          {user ? `Signed in as ${user.name?.split(' ')[0]}` : 'Guest mode — sign in to save history'}
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <div className="flex items-center justify-between border-b border-dark-600 px-4 py-3 lg:hidden">
          <button
            onClick={() => setMobileSidebarOpen(true)}
            className="rounded-lg p-2 text-gray-400 hover:bg-dark-700 hover:text-gold-400"
          >
            <Menu className="h-5 w-5" />
          </button>
          <div className="flex items-center gap-2 text-sm font-medium text-gray-300">
            <Scale className="h-4 w-4 text-gold-500" />
            LAWAI Chat
          </div>
          <button
            onClick={() => setSourceDrawerOpen((prev) => !prev)}
            className="rounded-lg p-2 text-gray-400 hover:bg-dark-700 hover:text-gold-400"
          >
            <PanelRight className="h-5 w-5" />
          </button>
        </div>

        <div className="flex min-h-0 flex-1">
          <div className="flex min-w-0 flex-1 flex-col">
            <div className="flex-1 overflow-y-auto px-4 py-6">
              <div className="mx-auto max-w-4xl space-y-6">
                {messages.length === 0 && (
                  <div className="flex h-full flex-col items-center justify-center py-12 text-center">
                    <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-gold-500/10">
                      <Scale className="h-10 w-10 text-gold-500" />
                    </div>
                    <h2 className="mb-3 font-serif text-2xl font-bold">Ask LAWAI Anything</h2>
                    <p className="mb-8 max-w-md text-gray-500">
                      Get instant answers on Indian law — IPC sections, constitutional rights,
                      family law, labour, tax, and more.
                    </p>
                    <div className="grid max-w-lg grid-cols-1 gap-3 sm:grid-cols-2">
                      {SUGGESTED_QUERIES.slice(0, 4).map((query) => (
                        <button
                          key={query}
                          onClick={() => sendMessage(query)}
                          className="card px-4 py-3 text-left text-sm transition-transform hover:-translate-y-0.5"
                        >
                          <span className="text-gray-300">{query}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex animate-slide-up ${
                      msg.role === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    {msg.role === 'user' ? (
                      <div className="max-w-2xl rounded-2xl rounded-tr-sm border border-gold-500/25 bg-gold-500/15 px-4 py-3 text-gray-200">
                        {msg.content}
                      </div>
                    ) : msg.role === 'error' ? (
                      <div className="flex max-w-2xl items-start gap-3 rounded-2xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-red-400">
                        <AlertCircle className="mt-0.5 h-5 w-5 flex-shrink-0" />
                        <span className="text-sm">{msg.content}</span>
                      </div>
                    ) : (
                      <div className="w-full max-w-3xl space-y-3">
                        <div className="flex items-center gap-3">
                          <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg bg-gold-500/20">
                            <Scale className="h-4 w-4 text-gold-500" />
                          </div>
                          {msg.domain && (
                            <span
                              className={`domain-badge ${DOMAIN_COLORS[msg.domain] || DOMAIN_COLORS.General}`}
                            >
                              {msg.domain} Law
                            </span>
                          )}
                          {msg.sources?.length > 0 && (
                            <button
                              onClick={() => {
                                setShowSources(showSources === msg.id ? null : msg.id)
                                setSourceDrawerOpen(true)
                              }}
                              className="ml-auto flex items-center gap-1 text-xs text-gold-400 transition-colors hover:text-gold-300"
                            >
                              <BookOpen className="h-3.5 w-3.5" />
                              {msg.sources.length} source{msg.sources.length > 1 ? 's' : ''}
                              <ChevronRight
                                className={`h-3.5 w-3.5 transition-transform ${
                                  showSources === msg.id ? 'rotate-90' : ''
                                }`}
                              />
                            </button>
                          )}
                        </div>
                        <div className="card prose prose-invert prose-sm max-w-none prose-headings:text-gold-400 prose-strong:text-gray-200 prose-code:text-gold-300">
                          <ReactMarkdown>{msg.content}</ReactMarkdown>
                        </div>
                        {showSources === msg.id && msg.sources?.length > 0 && (
                          <div className="space-y-2 border-l-2 border-gold-500/30 pl-4 xl:hidden">
                            {msg.sources.map((src, index) => (
                              <div key={`${msg.id}-source-${index}`} className="rounded-lg bg-dark-700 p-3 text-sm">
                                <div className="mb-1 flex items-center justify-between">
                                  <span className="font-medium text-gold-400">{src.title}</span>
                                  <span className="text-xs text-gray-500">{src.relevance}% match</span>
                                </div>
                                <p className="text-xs leading-relaxed text-gray-500">{src.snippet}</p>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}

                {loading && (
                  <div className="flex justify-start animate-fade-in">
                    <div className="flex items-center gap-3">
                      <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gold-500/20">
                        <Scale className="h-4 w-4 text-gold-500" />
                      </div>
                      <div className="card flex items-center gap-3 px-4 py-3">
                        <Loader2 className="h-4 w-4 animate-spin text-gold-500" />
                        <span className="text-sm text-gray-400">Analyzing legal corpus...</span>
                      </div>
                    </div>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>
            </div>

            <div className="border-t border-dark-600 p-4">
              <div className="mx-auto max-w-4xl">
                <div className="flex gap-3">
                  <textarea
                    ref={inputRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKey}
                    placeholder="Ask about any aspect of Indian law..."
                    rows={1}
                    className="input-field min-h-[48px] max-h-32 flex-1 resize-none py-3"
                    style={{ height: 'auto' }}
                    onInput={(e) => {
                      e.target.style.height = 'auto'
                      e.target.style.height = `${e.target.scrollHeight}px`
                    }}
                  />
                  <button
                    onClick={() => sendMessage()}
                    disabled={!input.trim() || loading}
                    className="btn-gold flex h-12 items-center justify-center px-4 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    <Send className="h-5 w-5" />
                  </button>
                </div>
                <p className="mt-2 text-center text-xs text-gray-600">
                  LAWAI provides general legal information. Always consult a qualified lawyer for
                  case-specific legal advice.
                </p>
              </div>
            </div>
          </div>

          <aside
            className={`${
              sourceDrawerOpen ? 'hidden xl:flex' : 'hidden'
            } w-80 flex-col border-l border-dark-600 bg-dark-800/50 p-4`}
          >
            <div className="mb-4 flex items-center gap-2">
              <BookOpen className="h-4 w-4 text-gold-500" />
              <h3 className="font-semibold text-white">Sources & Provenance</h3>
            </div>

            {activeSources.length > 0 ? (
              <div className="space-y-3 overflow-y-auto">
                {activeSources.map((src, index) => (
                  <div key={`panel-source-${index}`} className="rounded-xl border border-dark-600 bg-dark-700/70 p-4">
                    <div className="mb-2 flex items-start justify-between gap-3">
                      <div>
                        <h4 className="text-sm font-semibold text-gold-400">{src.title}</h4>
                        {src.section && <p className="text-xs text-gray-500">{src.section}</p>}
                      </div>
                      <span className="rounded-full bg-gold-500/10 px-2 py-1 text-xs text-gold-400">
                        {src.relevance}%
                      </span>
                    </div>
                    <p className="mb-2 text-xs text-gray-400">{src.domain}</p>
                    <p className="text-sm leading-relaxed text-gray-500">{src.snippet}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="rounded-xl border border-dashed border-dark-600 p-6 text-center text-sm text-gray-500">
                Ask a question to see cited sections, articles, and snippets here.
              </div>
            )}
          </aside>
        </div>
      </div>
    </div>
  )
}
