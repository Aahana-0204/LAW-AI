import { useState, useEffect } from 'react'
import { FileOutput, Wand2, Copy, Download, Loader2, CheckCircle, PenLine, ChevronDown } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '../services/api'

export default function GeneratePage() {
  const [templates, setTemplates] = useState([])
  const [selected, setSelected] = useState(null)
  const [fields, setFields] = useState({})
  const [customPrompt, setCustomPrompt] = useState('')
  const [useCustom, setUseCustom] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [result, setResult] = useState(null)
  const [copied, setCopied] = useState(false)

  useEffect(() => { fetchTemplates() }, [])

  const fetchTemplates = async () => {
    try {
      const { data } = await api.get('/generate/templates')
      setTemplates(data.templates || [])
    } catch {}
  }

  const selectTemplate = (t) => {
    setSelected(t)
    setFields({})
    setResult(null)
    setUseCustom(false)
  }

  const generate = async () => {
    if (generating) return
    if (!useCustom && !selected) { toast.error('Select a template first'); return }
    if (useCustom && !customPrompt.trim()) { toast.error('Enter a description'); return }
    if (!useCustom && selected) {
      const missing = (selected.fields || []).filter(f => !fields[f]?.trim())
      if (missing.length > 0) {
        toast.error(`Fill in: ${missing.slice(0, 3).map(f => f.replace(/_/g, ' ')).join(', ')}`)
        return
      }
    }
    setGenerating(true)
    setResult(null)
    try {
      const payload = useCustom
        ? { template_id: 'custom', fields: {}, custom_prompt: customPrompt }
        : { template_id: selected.id, fields }
      const { data } = await api.post('/generate/document', payload)
      setResult(data)
      toast.success('✅ Document generated!')
    } catch (err) {
      toast.error(err.response?.data?.error || 'Generation failed')
    } finally {
      setGenerating(false)
    }
  }

  const copy = () => {
    if (!result?.content) return
    navigator.clipboard.writeText(result.content)
    setCopied(true)
    toast.success('Copied!')
    setTimeout(() => setCopied(false), 2000)
  }

  const download = () => {
    if (!result?.content) return
    const blob = new Blob([result.content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${(result.template_name || 'document').replace(/\s+/g, '_')}_LAWAI.txt`
    a.click()
    URL.revokeObjectURL(url)
    toast.success('Downloaded!')
  }

  const fieldLabel = (f) => f.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())

  const textareaFields = new Set([
    'details', 'statements', 'information_sought', 'complaint_details',
    'assets_distribution', 'incident_details', 'scope', 'purpose',
  ])

  return (
    <div className="min-h-screen bg-dark-900 pt-20 px-4 pb-10">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-gold-500/20 bg-gold-500/10 px-4 py-1.5 text-sm text-gold-400 mb-4">
            <Wand2 className="h-3.5 w-3.5" />
            AI Powered · 100% Free
          </div>
          <h1 className="font-serif text-4xl font-bold gradient-text mb-2">Legal Document Generator</h1>
          <p className="text-gray-400 text-lg">Generate professional Indian legal documents in seconds</p>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          {/* Left: Input */}
          <div className="space-y-5">
            {/* Mode Toggle */}
            <div className="glass rounded-2xl p-1 flex gap-1">
              <button
                onClick={() => { setUseCustom(false); setResult(null) }}
                className={`flex-1 py-3 rounded-xl text-sm font-semibold transition-all ${!useCustom ? 'bg-gold-500/20 text-gold-400 shadow-inner' : 'text-gray-500 hover:text-gray-300'}`}
              >
                📋 Use Template
              </button>
              <button
                onClick={() => { setUseCustom(true); setResult(null) }}
                className={`flex-1 py-3 rounded-xl text-sm font-semibold transition-all ${useCustom ? 'bg-gold-500/20 text-gold-400 shadow-inner' : 'text-gray-500 hover:text-gray-300'}`}
              >
                ✍️ Custom Request
              </button>
            </div>

            {useCustom ? (
              <div className="glass rounded-2xl p-5 space-y-4">
                <label className="text-sm font-semibold text-gray-300 flex items-center gap-2">
                  <PenLine className="h-4 w-4 text-gold-400" />
                  Describe the document you need
                </label>
                <textarea
                  rows={6}
                  value={customPrompt}
                  onChange={e => setCustomPrompt(e.target.value)}
                  placeholder="e.g. Generate a rental agreement for a 2BHK flat in Mumbai between Rahul Sharma (landlord) and Priya Patel (tenant) for ₹25,000/month for 11 months starting August 2025, with 2 months security deposit..."
                  className="w-full bg-dark-700/60 border border-dark-600 rounded-xl px-4 py-3 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-gold-500/50 resize-none leading-relaxed"
                />
                <div className="flex flex-wrap gap-2">
                  {['Rental Agreement', 'NDA', 'Legal Notice', 'Affidavit', 'Will & Testament', 'RTI Application'].map(ex => (
                    <button
                      key={ex}
                      onClick={() => setCustomPrompt(`Generate a ${ex} `)}
                      className="text-xs px-3 py-1.5 rounded-full bg-dark-700 hover:bg-dark-600 text-gray-400 hover:text-gold-400 transition-colors border border-dark-600"
                    >
                      {ex}
                    </button>
                  ))}
                </div>
                <p className="text-xs text-gray-600">💡 Be specific — include names, dates, amounts, location, and any special terms.</p>
              </div>
            ) : (
              <>
                {/* Template Grid */}
                <div className="grid grid-cols-2 gap-3">
                  {templates.map(t => (
                    <button
                      key={t.id}
                      onClick={() => selectTemplate(t)}
                      className={`rounded-xl p-4 text-left transition-all border group ${
                        selected?.id === t.id
                          ? 'bg-gold-500/15 border-gold-500/40 shadow-lg shadow-gold-500/10'
                          : 'bg-dark-800/60 border-dark-600 hover:border-dark-500 hover:bg-dark-700/60'
                      }`}
                    >
                      <span className="text-2xl">{t.icon}</span>
                      <p className={`mt-2 text-sm font-semibold ${selected?.id === t.id ? 'text-gold-400' : 'text-gray-300 group-hover:text-gold-400'} transition-colors`}>
                        {t.name}
                      </p>
                      <p className="text-xs text-gray-600 mt-0.5 leading-relaxed">{t.description}</p>
                    </button>
                  ))}
                </div>

                {/* Dynamic Fields */}
                {selected && (
                  <div className="glass rounded-2xl p-5 space-y-4">
                    <h3 className="font-semibold text-gray-300 flex items-center gap-2">
                      <span className="text-xl">{selected.icon}</span>
                      {selected.name}
                      <span className="ml-auto text-xs text-gray-600">{selected.fields?.length} fields</span>
                    </h3>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {(selected.fields || []).map(f => (
                        <div key={f} className={textareaFields.has(f) ? 'sm:col-span-2' : ''}>
                          <label className="text-xs text-gray-500 mb-1.5 block font-medium">
                            {fieldLabel(f)} <span className="text-gold-500">*</span>
                          </label>
                          {textareaFields.has(f) ? (
                            <textarea
                              rows={3}
                              value={fields[f] || ''}
                              onChange={e => setFields(p => ({ ...p, [f]: e.target.value }))}
                              placeholder={`Enter ${fieldLabel(f).toLowerCase()}...`}
                              className="w-full bg-dark-700/60 border border-dark-600 rounded-xl px-3 py-2.5 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-gold-500/50 resize-none"
                            />
                          ) : (
                            <input
                              value={fields[f] || ''}
                              onChange={e => setFields(p => ({ ...p, [f]: e.target.value }))}
                              placeholder={`Enter ${fieldLabel(f).toLowerCase()}`}
                              className="w-full bg-dark-700/60 border border-dark-600 rounded-xl px-3 py-2.5 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-gold-500/50"
                            />
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}

            {/* Generate Button */}
            <button
              onClick={generate}
              disabled={generating || (!useCustom && !selected) || (useCustom && !customPrompt.trim())}
              className="btn-gold w-full py-4 rounded-xl font-bold text-base flex items-center justify-center gap-3 disabled:opacity-40 disabled:cursor-not-allowed transition-all hover:scale-[1.01] active:scale-[0.99] shadow-lg shadow-gold-500/20"
            >
              {generating ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Generating Document...
                </>
              ) : (
                <>
                  <Wand2 className="h-5 w-5" />
                  Generate Legal Document
                </>
              )}
            </button>

            {generating && (
              <p className="text-center text-xs text-gray-600 animate-pulse">
                ⚖️ AI is drafting your document with Indian legal standards… this may take 30–90 seconds
              </p>
            )}

            {/* Info Cards */}
            <div className="grid grid-cols-3 gap-3">
              {[
                { icon: '🇮🇳', label: 'Indian Law', sub: 'IPC, Contract Act, etc.' },
                { icon: '🤖', label: '100% Free', sub: 'Local AI, no API keys' },
                { icon: '⚡', label: '10 Templates', sub: 'RTI, FIR, NDA & more' },
              ].map(c => (
                <div key={c.label} className="rounded-xl bg-dark-800/60 border border-dark-700 px-3 py-3 text-center">
                  <div className="text-xl mb-1">{c.icon}</div>
                  <p className="text-xs font-semibold text-gray-300">{c.label}</p>
                  <p className="text-xs text-gray-600 mt-0.5">{c.sub}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Right: Output */}
          <div className="glass rounded-2xl overflow-hidden flex flex-col" style={{ minHeight: '600px' }}>
            <div className="px-5 py-4 border-b border-white/10 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-full bg-gold-500/20 flex items-center justify-center">
                  <FileOutput className="h-4 w-4 text-gold-400" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-200">{result ? result.template_name : 'Generated Document'}</h3>
                  {result && <p className="text-xs text-green-400">✅ Ready to download</p>}
                </div>
              </div>
              {result && (
                <div className="flex gap-2">
                  <button
                    onClick={copy}
                    className="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs bg-dark-700 hover:bg-dark-600 text-gray-300 transition-colors"
                  >
                    {copied ? <CheckCircle className="h-3.5 w-3.5 text-green-400" /> : <Copy className="h-3.5 w-3.5" />}
                    {copied ? 'Copied!' : 'Copy'}
                  </button>
                  <button
                    onClick={download}
                    className="flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs bg-gold-500/20 hover:bg-gold-500/30 text-gold-400 transition-colors"
                  >
                    <Download className="h-3.5 w-3.5" />
                    Download .txt
                  </button>
                </div>
              )}
            </div>

            <div className="flex-1 overflow-y-auto p-5">
              {!result && !generating && (
                <div className="flex flex-col items-center justify-center h-full text-center gap-5 py-16">
                  <div className="relative">
                    <div className="h-24 w-24 rounded-full bg-gold-500/10 flex items-center justify-center">
                      <FileOutput className="h-12 w-12 text-gold-400 opacity-30" />
                    </div>
                  </div>
                  <div>
                    <p className="text-gray-400 font-semibold mb-2">Your legal document will appear here</p>
                    <p className="text-gray-600 text-sm mb-4">Select a template, fill in details, and click Generate</p>
                  </div>
                  <div className="w-full max-w-xs space-y-2 text-left">
                    {[
                      '📄 Properly formatted under Indian law',
                      '⚖️ All standard legal clauses included',
                      '✍️ Signature blocks for all parties',
                      '📥 Download as text file',
                    ].map(f => (
                      <div key={f} className="flex items-center gap-2 text-xs text-gray-600">
                        <span>{f}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {generating && (
                <div className="flex flex-col items-center justify-center h-full gap-6">
                  <div className="relative">
                    <div className="h-24 w-24 rounded-full border-4 border-gold-500/20 border-t-gold-400 animate-spin" />
                    <div className="absolute inset-0 flex items-center justify-center">
                      <Wand2 className="h-10 w-10 text-gold-400" />
                    </div>
                  </div>
                  <div className="text-center">
                    <p className="text-gold-400 font-semibold mb-1 animate-pulse">Drafting your document...</p>
                    <p className="text-gray-600 text-sm">AI applying Indian legal standards & clauses</p>
                  </div>
                  <div className="flex gap-1">
                    {[0, 1, 2].map(i => (
                      <div key={i} className="h-2 w-2 bg-gold-400 rounded-full animate-bounce"
                        style={{ animationDelay: `${i * 0.2}s` }} />
                    ))}
                  </div>
                </div>
              )}

              {result?.content && (
                <div className="bg-dark-800/40 rounded-xl border border-dark-600 overflow-hidden">
                  <div className="bg-dark-800 px-5 py-3 border-b border-dark-600 flex items-center gap-2">
                    <span className="text-xs text-gold-400 font-semibold uppercase tracking-wider">⚖️ LAWAI • Legal Document</span>
                    <span className="ml-auto text-xs text-gray-600">{result.content.length.toLocaleString()} chars</span>
                  </div>
                  <div className="p-5">
                    <pre className="text-sm text-gray-300 whitespace-pre-wrap font-mono leading-relaxed">
                      {result.content}
                    </pre>
                  </div>
                  <div className="bg-yellow-500/5 border-t border-yellow-500/10 px-5 py-3">
                    <p className="text-xs text-yellow-500/60 text-center">
                      ⚠️ AI-generated draft for reference only. Consult a qualified lawyer before use.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
