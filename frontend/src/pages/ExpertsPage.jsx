import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Calendar, CheckCircle, Clock, Star, X } from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'

const DOMAINS_FILTER = [
  'All',
  'Criminal',
  'Civil',
  'Constitutional',
  'Family',
  'Property',
  'Labour',
  'Corporate',
  'Tax',
]

const TIME_SLOTS = ['9:00 AM', '10:00 AM', '11:00 AM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM']

export default function ExpertsPage() {
  const [experts, setExperts] = useState([])
  const [domain, setDomain] = useState('All')
  const [loading, setLoading] = useState(true)
  const [bookingExpert, setBookingExpert] = useState(null)
  const [booking, setBooking] = useState({ date: '', time_slot: '', query_summary: '' })
  const [bookingLoading, setBookingLoading] = useState(false)
  const [booked, setBooked] = useState(false)
  const { user } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    fetchExperts()
  }, [domain])

  const fetchExperts = async () => {
    setLoading(true)
    try {
      const params = domain !== 'All' ? { domain } : {}
      const res = await api.get('/api/experts/', { params })
      setExperts(res.data.experts || [])
    } catch {
      toast.error('Failed to load experts')
    } finally {
      setLoading(false)
    }
  }

  const handleBook = async () => {
    if (!user) {
      navigate('/login')
      return
    }
    if (!booking.date || !booking.time_slot) {
      toast.error('Select date and time')
      return
    }
    setBookingLoading(true)
    try {
      await api.post('/api/experts/book', { expert_id: bookingExpert._id, ...booking })
      setBooked(true)
      toast.success('Booking confirmed! 🎉')
    } catch (err) {
      toast.error(err.response?.data?.error || 'Booking failed')
    } finally {
      setBookingLoading(false)
    }
  }

  return (
    <div className="min-h-screen px-4 pt-20">
      <div className="mx-auto max-w-6xl">
        <div className="mb-10 text-center">
          <h1 className="mb-3 font-serif text-4xl font-bold">
            Legal <span className="gradient-text">Experts</span>
          </h1>
          <p className="text-gray-400">
            Connect with verified lawyers for professional legal guidance.
          </p>
        </div>

        <div className="mb-8 flex flex-wrap justify-center gap-2">
          {DOMAINS_FILTER.map((item) => (
            <button
              key={item}
              onClick={() => setDomain(item)}
              className={`rounded-full px-4 py-1.5 text-sm font-medium transition-all ${
                domain === item
                  ? 'bg-gold-500 text-dark-900'
                  : 'border border-dark-500 text-gray-400 glass hover:text-gold-400'
              }`}
            >
              {item}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="flex justify-center py-20">
            <div className="h-8 w-8 animate-spin rounded-full border-2 border-gold-500/30 border-t-gold-500" />
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {experts.map((expert) => (
              <div key={expert._id} className="card flex flex-col">
                <div className="mb-4 flex items-start gap-4">
                  <div className="flex h-14 w-14 flex-shrink-0 items-center justify-center rounded-xl bg-gold-500/20 text-lg font-bold text-gold-400">
                    {expert.avatar}
                  </div>
                  <div>
                    <h3 className="font-semibold text-white">{expert.name}</h3>
                    <p className="text-sm text-gold-400">{expert.specialization}</p>
                    <div className="mt-1 flex items-center gap-1">
                      <Star className="h-3.5 w-3.5 fill-gold-500 text-gold-500" />
                      <span className="text-sm text-gray-300">{expert.rating}</span>
                      <span className="ml-2 text-xs text-gray-600">{expert.experience} yrs exp</span>
                    </div>
                  </div>
                </div>
                <p className="mb-4 flex-1 text-sm text-gray-500">{expert.bio}</p>
                <div className="mb-4 flex items-center justify-between">
                  <span className="text-lg font-bold text-white">
                    ₹{expert.fee}
                    <span className="text-sm font-normal text-gray-500">/session</span>
                  </span>
                  <span
                    className={`rounded-full border px-2.5 py-1 text-xs font-medium ${
                      expert.available
                        ? 'border-green-500/30 bg-green-500/15 text-green-400'
                        : 'border-gray-500/30 bg-gray-500/15 text-gray-500'
                    }`}
                  >
                    {expert.available ? '● Available' : '○ Unavailable'}
                  </span>
                </div>
                <button
                  onClick={() => {
                    if (!expert.available) return
                    setBookingExpert(expert)
                    setBooked(false)
                    setBooking({ date: '', time_slot: '', query_summary: '' })
                  }}
                  disabled={!expert.available}
                  className={`w-full rounded-lg py-2.5 text-sm font-medium transition-all ${
                    expert.available ? 'btn-gold' : 'cursor-not-allowed bg-dark-700 text-gray-600'
                  }`}
                >
                  {expert.available ? 'Book Consultation' : 'Not Available'}
                </button>
              </div>
            ))}
          </div>
        )}

        {bookingExpert && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4 backdrop-blur-sm">
            <div className="w-full max-w-md animate-slide-up rounded-2xl border border-dark-600 bg-dark-800 p-6">
              {booked ? (
                <div className="py-6 text-center">
                  <CheckCircle className="mx-auto mb-4 h-16 w-16 text-green-400" />
                  <h3 className="mb-2 text-xl font-bold">Booking Confirmed!</h3>
                  <p className="mb-6 text-sm text-gray-400">
                    Your consultation with {bookingExpert.name} has been scheduled.
                  </p>
                  <button onClick={() => setBookingExpert(null)} className="btn-gold">
                    Done
                  </button>
                </div>
              ) : (
                <>
                  <div className="mb-6 flex items-center justify-between">
                    <h3 className="text-lg font-bold">Book Consultation</h3>
                    <button
                      onClick={() => setBookingExpert(null)}
                      className="rounded-lg p-1 text-gray-500 hover:text-gray-300"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  </div>
                  <div className="mb-6 flex items-center gap-3 rounded-lg bg-dark-700 p-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gold-500/20 font-bold text-gold-400">
                      {bookingExpert.avatar}
                    </div>
                    <div>
                      <p className="text-sm font-medium">{bookingExpert.name}</p>
                      <p className="text-xs text-gold-400">
                        {bookingExpert.specialization} • ₹{bookingExpert.fee}
                      </p>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div>
                      <label className="mb-1.5 block text-sm font-medium text-gray-400">
                        <Calendar className="mr-1 inline h-4 w-4" />
                        Select Date
                      </label>
                      <input
                        type="date"
                        value={booking.date}
                        min={new Date().toISOString().split('T')[0]}
                        onChange={(e) => setBooking({ ...booking, date: e.target.value })}
                        className="input-field"
                      />
                    </div>
                    <div>
                      <label className="mb-1.5 block text-sm font-medium text-gray-400">
                        <Clock className="mr-1 inline h-4 w-4" />
                        Time Slot
                      </label>
                      <div className="grid grid-cols-3 gap-2">
                        {TIME_SLOTS.map((slot) => (
                          <button
                            key={slot}
                            onClick={() => setBooking({ ...booking, time_slot: slot })}
                            className={`rounded-lg border py-2 text-sm transition-all ${
                              booking.time_slot === slot
                                ? 'border-gold-500 bg-gold-500/20 text-gold-400'
                                : 'border-dark-500 text-gray-500 hover:border-gold-500/40'
                            }`}
                          >
                            {slot}
                          </button>
                        ))}
                      </div>
                    </div>
                    <div>
                      <label className="mb-1.5 block text-sm font-medium text-gray-400">
                        Brief Query (optional)
                      </label>
                      <textarea
                        value={booking.query_summary}
                        onChange={(e) => setBooking({ ...booking, query_summary: e.target.value })}
                        className="input-field resize-none"
                        rows={2}
                        placeholder="Describe your legal issue briefly..."
                      />
                    </div>
                    <button
                      onClick={handleBook}
                      disabled={bookingLoading || !booking.date || !booking.time_slot}
                      className="btn-gold flex w-full items-center justify-center gap-2 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      {bookingLoading ? (
                        <div className="h-4 w-4 animate-spin rounded-full border-2 border-dark-900/30 border-t-dark-900" />
                      ) : (
                        'Confirm Booking'
                      )}
                    </button>
                    {!user && (
                      <p className="text-center text-xs text-gray-500">
                        You&apos;ll need to sign in to complete the booking.
                      </p>
                    )}
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
