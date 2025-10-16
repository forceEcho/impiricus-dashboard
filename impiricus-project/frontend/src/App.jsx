import React, { useState, useEffect } from 'react';
import { Search, AlertCircle } from 'lucide-react';

export default function MessageDashboard() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [physicianFilter, setPhysicianFilter] = useState('');
  const [classificationResults, setClassificationResults] = useState({});
  const [classifyingIds, setClassifyingIds] = useState(new Set());

  const API_BASE = 'http://localhost:8000';

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async (physicianId = null) => {
    setLoading(true);
    setError(null);
    try {
      const url = physicianId 
        ? `${API_BASE}/messages/?physician=${physicianId}`
        : `${API_BASE}/messages/`;
      
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch messages');
      
      const data = await response.json();
      setMessages(data.data || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    const physicianId = physicianFilter.trim();
    fetchMessages(physicianId || null);
  };

  const handleClearFilter = () => {
    setPhysicianFilter('');
    fetchMessages();
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const classifyMessage = async (messageId) => {
    setClassifyingIds(prev => new Set(prev).add(messageId));
    try {
      const response = await fetch(`${API_BASE}/classify/${messageId}`, {
        method: 'POST'
      });
      
      if (!response.ok) throw new Error('Classification failed');
      
      const data = await response.json();
      setClassificationResults(prev => ({
        ...prev,
        [messageId]: data.message
      }));
    } catch (err) {
      setClassificationResults(prev => ({
        ...prev,
        [messageId]: `Error: ${err.message}`
      }));
    } finally {
      setClassifyingIds(prev => {
        const next = new Set(prev);
        next.delete(messageId);
        return next;
      });
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Message Management Dashboard
        </h1>

        {/* Filter Section */}
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <div className="flex gap-3">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Filter by Physician ID
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={physicianFilter}
                  onChange={(e) => setPhysicianFilter(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Enter physician ID"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={handleSearch}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 flex items-center gap-2"
                >
                  <Search size={18} />
                  Search
                </button>
                {physicianFilter && (
                  <button
                    onClick={handleClearFilter}
                    className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
                  >
                    Clear
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-start gap-3">
            <AlertCircle className="text-red-600 flex-shrink-0" size={20} />
            <div>
              <h3 className="font-medium text-red-900">Error</h3>
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading messages...</p>
          </div>
        ) : (
          <>
            {/* Message Count */}
            <div className="mb-4 text-sm text-gray-600">
              Showing {messages.length} message{messages.length !== 1 ? 's' : ''}
            </div>

            {/* Messages Table */}
            <div className="bg-white rounded-lg shadow overflow-hidden">
              {messages.length === 0 ? (
                <div className="p-8 text-center text-gray-500">
                  No messages found
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-100 border-b border-gray-200">
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                          Physician ID
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                          Message
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                          Timestamp
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                          Topic
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                          Sentiment
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">
                          Action
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {messages.map((msg) => (
                        <React.Fragment key={msg.message_id}>
                          <tr className="hover:bg-gray-50">
                            <td className="px-4 py-3 text-sm text-gray-900">
                              {msg.physician_id}
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-700">
                              <div className="max-w-md truncate" title={msg.message_text}>
                                {msg.message_text}
                              </div>
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-600 whitespace-nowrap">
                              {formatTimestamp(msg.timestamp)}
                            </td>
                            <td className="px-4 py-3 text-sm text-gray-900">
                              {msg.topic || '-'}
                            </td>
                            <td className="px-4 py-3 text-sm">
                              {msg.sentiment ? (
                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                  msg.sentiment === 'positive' ? 'bg-green-100 text-green-800' :
                                  msg.sentiment === 'negative' ? 'bg-red-100 text-red-800' :
                                  'bg-gray-100 text-gray-800'
                                }`}>
                                  {msg.sentiment}
                                </span>
                              ) : '-'}
                            </td>
                            <td className="px-4 py-3 text-sm">
                              <button
                                onClick={() => classifyMessage(msg.message_id)}
                                disabled={classifyingIds.has(msg.message_id)}
                                className="px-3 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-xs font-medium"
                              >
                                {classifyingIds.has(msg.message_id) ? 'Classifying...' : 'Classify'}
                              </button>
                            </td>
                          </tr>
                          {classificationResults[msg.message_id] && (
                            <tr>
                              <td colSpan="6" className="px-4 py-2 bg-blue-50">
                                <div className="text-sm">
                                  <span className="font-medium text-blue-900">Classification: </span>
                                  <span className="text-blue-800">
                                    {classificationResults[msg.message_id]}
                                  </span>
                                </div>
                              </td>
                            </tr>
                          )}
                        </React.Fragment>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
