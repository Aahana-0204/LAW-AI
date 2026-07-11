import { useState, useRef, useCallback, useEffect } from 'react'
import { Upload, FileText, Trash2, Send, Bot, User, Loader2, X } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '../services/api'

export default function UploadPage() {
  const [files, setFiles] = useState([])
  const [uploading, setUploading] = useState(false)
  const [isDragging, setIsDragging] = useState(false)
  const [selectedDoc, setSelectedDoc] = useState(null)
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [thinking, setThinking] = useState(false)
  const fileRef = useRef(null)
  const bottomRef = useRef(null)

  useEffect(() => { fetchDocs() }, [])
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages])

  const fetchDocs = async () => {
    try {
      const { data } = await api.get('/docs/documents')
      setFiles(data.documents || [])
    } catch {}
  }

  const uploadFile = async (file) => {
    const allowedExt = ['pdf', 'docx', 'txt']
    const ext = file.name.split('.').pop().toLowerCase()
    if (!allowedExt.includes(ext)) {
      toast.error(`Unsupported: ${file.name}. Use PDF, DOCX, or TXT.`)
      return
    }
    if (file.size > 10 * 1024 * 1024) {
      toast.error('File too large. Max 10 MB.')
      return
    }
    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)
    try {
      const { data } = await api.post('/docs/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      toast.success(`✅ ${file.name} uploaded (${data.chunks} chunks)`)
      fetchDocs()
    } catch (err) {
      toast.error(err.response?.data?.error || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setIsDragging(false)
    Array.from(e.dataTransfer.files).forEach(uploadFile)
  }, [])

  const deleteDoc = async (docId, filename) => {
    try {
      await api.delete(`/docs/documents/${docId}`)
      toast.success(`Deleted ${filename}`)
      setFiles(f => f.filter(d => d.doc_id !== docId))
      if (selectedDoc?.doc_id === docId) setSelectedDoc(null)
    } catch {
      toast.error('Delete failed')
    }
  }

  const sendQuery = async (e) => {
    e.preventDefault()
    if (!input.trim() || thinking) return
    const q = input.trim()
    setInput('')
    setMessages(m => [...m, { role: 'user', content: q }])
    setThinking(true)
    try {
      const { data } = await api.post('/docs/query', {
        query: q,
        doc_id: selectedDoc?.doc_id || null,
      })
      setMessages(m => [...m, { role: 'assistant', content: data.answer, sources: data.sources }])
    } catch (err) {
      setMessages(m => [...m, {
        role: 'assistant',
        content: '❌ ' + (err.response?.data?.error || 'Query failed'),
        sources: [],
      }])
    } finally {
      setThinking(false)
    }
  }

  const fileIcon = (filename) => {
    const ext = filename.split('.').pop().toLowerCase()
    if (ext === 'pdf') return '📄'
    if (ext === 'docx' || ext === 'doc') return '📝'
    return '📃'
  }

  return (
    <div className="min-h-screen bg-dark-900 pt-20 px-4 pb-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-gold-500/20 bg-gold-500/10 px-4 py-1.5 text-sm text-gold-400 mb-4">
            <Upload className="h-3.5 w-3.5" />
            Document Intelligence
          </div>
          <h1 className="font-serif text-4xl font-bold gradient-text mb-2">My Legal Documents</h1>
          <p className="text-gray-400 text-lg">Upload contracts, agreements, notices — ask anything about them</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6" style={{ minHeight: '70vh' }}>
          {/* Left Panel */}
          <div className="lg:col-span-1 flex flex-col gap-4">
            {/* Upload Zone */}
            <div
              className={`relative rounded-2xl border-2 border-dashed p-8 text-center cursor-pointer transition-all duration-300 ${
                isDragging
                  ? 'border-gold-400 bg-gold-500/10 scale-[1.02] shadow-lg shadow-gold-500/20'
                  : 'border-dark-600 hover:border-gold-500/50 bg-dark-800/50'
              }`}
              onDragOver={e => { e.preventDefault(); setIsDragging(true) }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
              onClick={() => fileRef.current?.click()}
            >
              <input
                ref={fileRef}
                type="file"
                className="hidden"
                accept=".pdf,.docx,.txt"
                multiple
                onChange={e => Array.from(e.target.files).forEach(uploadFile)}
              />
              {uploading ? (
                <div className="flex flex-col items-center gap-3">
                  <Loader2 className="h-12 w-12 text-gold-400 animate-spin" />
                  <p className="text-gold-400 font-semibold">Processing document...</p>
                  <p className="text-xs text-gray-500">Indexing into vector DB</p>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-3">
                  <div className={`h-14 w-14 rounded-full flex items-center justify-center transition-colors ${isDragging ? 'bg-gold-500/20' : 'bg-dark-700'}`}>
                    <Upload className={`h-7 w-7 ${isDragging ? 'text-gold-400' : 'text-gray-500'}`} />
                  </div>
                  <div>
                    <p className="font-semibold text-gray-300">
                      {isDragging ? '✨ Drop to upload!' : 'Drag & drop files here'}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">or click to browse</p>
                  </div>
                  <div className="flex gap-2 mt-1">
                    {['PDF', 'DOCX', 'TXT'].map(t => (
                      <span key={t} className="text-xs px-2 py-0.5 rounded bg-dark-700 text-gray-500">{t}</span>
                    ))}
                  </div>
                  <p className="text-xs text-gray-600">Max 10 MB per file</p>
                </div>
              )}
            </div>

            {/* File List */}
            <div className="flex-1 flex flex-col">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Uploaded Documents</h3>
                <span className="text-xs text-gray-600 bg-dark-800 rounded-full px-2 py-0.5">{files.length}</span>
              </div>

              {files.length === 0 ? (
                <div className="flex-1 flex flex-col items-center justify-center text-center py-8 rounded-xl border border-dashed border-dark-700">
                  <FileText className="h-10 w-10 text-gray-700 mb-2" />
                  <p className="text-sm text-gray-600">No documents yet</p>
                  <p className="text-xs text-gray-700 mt-1">Upload to start analyzing</p>
                </div>
              ) : (
                <div className="space-y-2 flex-1 overflow-y-auto pr-1">
                  {files.map(doc => (
                    <div
                      key={doc.doc_id}
                      onClick={() => setSelectedDoc(selectedDoc?.doc_id === doc.doc_id ? null : doc)}
                      className={`group flex items-center gap-3 rounded-xl p-3 cursor-pointer transition-all border ${
                        selectedDoc?.doc_id === doc.doc_id
                          ? 'bg-gold-500/10 border-gold-500/30 shadow-md shadow-gold-500/10'
                          : 'bg-dark-800/60 hover:bg-dark-700/60 border-transparent hover:border-dark-600'
                      }`}
                    >
                      <span className="text-2xl flex-shrink-0">{fileIcon(doc.filename)}</span>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-200 truncate">{doc.filename}</p>
                        <p className="text-xs text-gray-500">{doc.total_chunks} chunks indexed</p>
                      </div>
                      <button
                        onClick={ev => { ev.stopPropagation(); deleteDoc(doc.doc_id, doc.filename) }}
                        className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg text-red-400 hover:bg-red-500/10 transition-all flex-shrink-0"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  ))}
                </div>
              )}

              {selectedDoc && (
                <div className="mt-3 rounded-xl bg-gold-500/10 border border-gold-500/20 px-4 py-3 flex items-center justify-between">
                  <div>
                    <p className="text-xs text-gold-400 font-semibold">Filtering by:</p>
                    <p className="text-xs text-gray-400 truncate max-w-[150px]">{selectedDoc.filename}</p>
                  </div>
                  <button onClick={() => setSelectedDoc(null)} className="text-gray-500 hover:text-gray-300">
                    <X className="h-4 w-4" />
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Right: Chat Interface */}
          <div className="lg:col-span-2 glass rounded-2xl flex flex-col overflow-hidden" style={{ minHeight: '500px' }}>
            <div className="px-5 py-4 border-b border-white/10 flex items-center gap-3">
              <div className="h-9 w-9 rounded-full bg-gradient-to-br from-gold-500/30 to-amber-600/30 flex items-center justify-center">
                <Bot className="h-5 w-5 text-gold-400" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-200">Document AI Assistant</h3>
                <p className="text-xs text-gray-500">
                  {selectedDoc
                    ? `Analyzing: ${selectedDoc.filename}`
                    : files.length > 0
                      ? `Searching across all ${files.length} document(s)`
                      : 'Upload documents to start'}
                </p>
              </div>
              {files.length > 0 && (
                <div className="ml-auto flex items-center gap-1.5">
                  <div className="h-2 w-2 bg-green-400 rounded-full animate-pulse" />
                  <span className="text-xs text-green-400">Ready</span>
                </div>
              )}
            </div>

            <div className="flex-1 overflow-y-auto p-5 space-y-4">
              {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full text-center gap-5 py-12">
                  <div className="relative">
                    <div className="h-20 w-20 rounded-full bg-gold-500/10 flex items-center justify-center">
                      <FileText className="h-10 w-10 text-gold-400 opacity-50" />
                    </div>
                    <div className="absolute -bottom-1 -right-1 h-7 w-7 bg-green-500/20 rounded-full flex items-center justify-center">
                      <Bot className="h-4 w-4 text-green-400" />
                    </div>
                  </div>
                  <div className="max-w-sm">
                    <p className="text-gray-300 font-semibold mb-2">Ask about your legal documents</p>
                    <p className="text-gray-600 text-sm leading-relaxed">
                      Upload contracts, agreements, notices, or court orders — then ask anything like:
                    </p>
                    <div className="mt-3 space-y-2">
                      {[
                        '"What are the notice period terms?"',
                        '"Summarize the key obligations"',
                        '"Are there any penalty clauses?"',
                      ].map(q => (
                        <div key={q} className="text-xs bg-dark-800/80 rounded-lg px-3 py-2 text-gray-500 italic">{q}</div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {messages.map((msg, i) => (
                <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  {msg.role === 'assistant' && (
                    <div className="h-8 w-8 rounded-full bg-gold-500/20 flex items-center justify-center flex-shrink-0 mt-1">
                      <Bot className="h-4 w-4 text-gold-400" />
                    </div>
                  )}
                  <div className="max-w-[80%]">
                    <div className={`rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap ${
                      msg.role === 'user'
                        ? 'bg-gold-500/20 text-gray-200 rounded-tr-sm'
                        : 'bg-dark-700/80 text-gray-300 rounded-tl-sm'
                    }`}>
                      {msg.content}
                    </div>
                    {msg.sources?.length > 0 && (
                      <div className="mt-2 space-y-1">
                        {msg.sources.slice(0, 3).map((s, j) => (
                          <div key={j} className="text-xs text-gray-600 bg-dark-800/50 rounded-lg px-3 py-1.5 flex items-center gap-2">
                            <span>📄</span>
                            <span className="truncate">{s.filename}</span>
                            <span className="text-gray-700 flex-shrink-0">chunk {s.chunk} · {s.relevance}%</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                  {msg.role === 'user' && (
                    <div className="h-8 w-8 rounded-full bg-dark-700 flex items-center justify-center flex-shrink-0 mt-1">
                      <User className="h-4 w-4 text-gray-400" />
                    </div>
                  )}
                </div>
              ))}

              {thinking && (
                <div className="flex gap-3">
                  <div className="h-8 w-8 rounded-full bg-gold-500/20 flex items-center justify-center">
                    <Bot className="h-4 w-4 text-gold-400" />
                  </div>
                  <div className="bg-dark-700/80 rounded-2xl rounded-tl-sm px-4 py-3">
                    <div className="flex gap-1 items-center h-4">
                      {[0, 1, 2].map(i => (
                        <div key={i} className="h-2 w-2 bg-gold-400 rounded-full animate-bounce"
                          style={{ animationDelay: `${i * 0.15}s` }} />
                      ))}
                    </div>
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>

            <form onSubmit={sendQuery} className="p-4 border-t border-white/10 flex gap-3">
              <input
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder={files.length === 0 ? 'Upload a document first...' : 'Ask about your documents...'}
                disabled={files.length === 0 || thinking}
                className="flex-1 bg-dark-700/60 border border-dark-600 rounded-xl px-4 py-3 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-gold-500/50 disabled:opacity-40 transition-colors"
              />
              <button
                type="submit"
                disabled={!input.trim() || thinking || files.length === 0}
                className="btn-gold px-4 py-3 rounded-xl disabled:opacity-40 disabled:cursor-not-allowed transition-all hover:scale-105 active:scale-95"
              >
                {thinking ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}
