import React, { useState, useEffect } from 'react';
import './index.css';

// Simple Inline SVGs for Premium Feel
const UploadIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
    <polyline points="17 8 12 3 7 8" />
    <line x1="12" y1="3" x2="12" y2="15" />
  </svg>
);

const FileIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
    <polyline points="13 2 13 9 20 9" />
  </svg>
);

const CheckIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="20 6 9 17 4 12" />
  </svg>
);

const SparkleIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
  </svg>
);

const TrendingUpIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
    <polyline points="17 6 23 6 23 12" />
  </svg>
);

const MenuIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="3" y1="12" x2="21" y2="12" />
    <line x1="3" y1="6" x2="21" y2="6" />
    <line x1="3" y1="18" x2="21" y2="18" />
  </svg>
);

const CloseIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </svg>
);

const ChevronLeftIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="15 18 9 12 15 6" />
  </svg>
);

// Stroke-free pixel-perfect QR Code
const QRCodeSVG = () => (
  <svg width="100" height="100" viewBox="0 0 29 29" fill="currentColor">
    <path d="M0 0h7v7H0zM22 0h7v7h-7zM0 22h7v7H0zM3 3h1v1H3zM25 3h1v1h-1zM3 25h1v1H3z" />
    <path d="M10 0h2v1h-2zM14 0h1v3h-1zM17 0h3v1h-3zM10 3h1v2h-1zM12 3h1v1h-1zM16 3h2v1h-2zM19 4h2v1h-2zM10 6h3v1h-3zM15 6h1v1h-1zM18 6h1v1h-1z" />
    <path d="M0 10h1v1H0zM3 10h1v2H3zM5 10h2v1H5zM9 10h3v1H9zM13 10h1v1h-1zM16 10h2v1h-2zM20 10h1v1h-1zM23 10h1v1h-1zM25 10h3v1h-3z" />
    <path d="M1 12h2v1H1zM5 12h1v1H5zM8 12h1v2H8zM11 12h1v1h-1zM14 12h2v1h-2zM18 12h1v1h-1zM21 12h3v1h-3zM26 12h2v1h-2z" />
    <path d="M0 15h3v1H0zM4 15h1v1H4zM7 15h1v1H7zM10 15h2v1h-2zM13 15h1v1h-1zM16 15h2v1h-2zM20 15h1v1h-1zM23 15h1v1h-1zM25 15h3v1h-3z" />
    <path d="M1 17h2v1H1zM5 17h1v1H5zM8 17h1v2H8zM11 17h1v1h-1zM14 17h2v1h-2zM18 17h1v1h-1zM21 17h3v1h-3zM26 17h2v1h-2z" />
    <path d="M10 20h2v1h-2zM14 20h1v3h-1zM17 20h3v1h-3zM10 23h1v2h-1zM12 23h1v1h-1zM16 23h2v1h-2zM19 24h2v1h-2z" />
  </svg>
);

function App() {
  const [uploadState, setUploadState] = useState('idle'); // 'idle', 'uploading', 'done'
  const [progress, setProgress] = useState(0);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [expandedQuestion, setExpandedQuestion] = useState(null);
  const [isTheaterMode, setIsTheaterMode] = useState(false);
  const [copiedLink, setCopiedLink] = useState(false);
  
  const [activeLectureId, setActiveLectureId] = useState('current');
  const [activeLectureTitle, setActiveLectureTitle] = useState('Neural_Networks_Lec4.pdf');

  const [analysisData, setAnalysisData] = useState(null);
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);
  const [analysisError, setAnalysisError] = useState(null);
  
  const [lecturesList, setLecturesList] = useState([]);
  const [statsData, setStatsData] = useState(null);
  const [quizInfo, setQuizInfo] = useState(null);

  useEffect(() => {
    fetch('http://localhost:21679/lectures')
      .then(res => res.json())
      .then(data => setLecturesList(data))
      .catch(err => console.error("Failed to fetch lectures:", err));
  }, []);

  useEffect(() => {
    if (uploadState === 'done') {
      setLoadingAnalysis(true);
      const fetchId = activeLectureId === 'current' ? 1 : activeLectureId;
      
      fetch(`http://localhost:21679/quizzes/${fetchId}/analysis`)
        .then(res => {
          if (!res.ok) throw new Error('Failed to fetch analysis');
          return res.json();
        })
        .then(data => {
          setAnalysisData(data);
          setAnalysisError(null);
        })
        .catch(err => {
          console.error(err);
          setAnalysisError(err.message);
        })
        .finally(() => {
          setLoadingAnalysis(false);
        });

      fetch(`http://localhost:21679/quizzes/${fetchId}/stats`)
        .then(res => res.ok ? res.json() : null)
        .then(data => setStatsData(data))
        .catch(err => console.error(err));
        
      fetch(`http://localhost:21679/quizzes/${fetchId}`)
        .then(res => res.ok ? res.json() : null)
        .then(data => setQuizInfo(data))
        .catch(err => console.error(err));
    }
  }, [uploadState, activeLectureId]);



  // Handle fake upload
  const handleUpload = () => {
    if (uploadState !== 'idle') return;
    setUploadState('uploading');
    setProgress(0);
    
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setUploadState('done');
          return 100;
        }
        return prev + 5;
      });
    }, 100);
  };

  // Keyboard accessibility triggers
  const handleQuestionKeyDown = (e, itemId) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      setExpandedQuestion(expandedQuestion === itemId ? null : itemId);
    }
  };

  const handleUploadKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleUpload();
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText("check.lec/4921");
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2000);
  };

  const handlePastUploadClick = (file, e) => {
    e.preventDefault();
    setActiveLectureId(file.id);
    setActiveLectureTitle(file.title);
    setUploadState('done');
    if (isSidebarOpen) setIsSidebarOpen(false);
  };

  const handleCurrentUploadClick = (e) => {
    e.preventDefault();
    setActiveLectureId('current');
    setActiveLectureTitle('Neural_Networks_Lec4.pdf');
    if (isSidebarOpen) setIsSidebarOpen(false);
  };

  // Helper to determine semantic colors for score ranges
  const getScoreColor = (correct) => {
    if (correct >= 80) return 'var(--color-feedback-success)';
    if (correct >= 50) return 'var(--color-feedback-warning)';
    return 'var(--color-feedback-error)';
  };

  return (
    <div className={`layout ${isSidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
      {/* Overlay background for mobile sidebar */}
      <div 
        className={`sidebar-overlay ${isSidebarOpen ? 'open' : ''}`}
        onClick={() => setIsSidebarOpen(false)}
        aria-hidden="true"
      ></div>

      {/* Sidebar for Past Uploads Library */}
      <aside id="sidebar" className={`sidebar ${isSidebarOpen ? 'open' : ''}`}>
        {/* Mobile close button */}
        <button 
          className="sidebar-close-btn"
          onClick={() => setIsSidebarOpen(false)}
          aria-label="Close menu"
        >
          <CloseIcon />
        </button>

        <div style={{ display: 'flex', alignItems: 'center', width: '100%' }}>
          <div className="brand">
            <div className="brand-icon">✓</div>
            <span className="brand-text">LectureCheck</span>
          </div>
          
          {/* Desktop Collapse tab (Chevron that flips 180 degrees) */}
          <button 
            className="collapse-toggle"
            onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
            title={isSidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            aria-label={isSidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            <ChevronLeftIcon />
          </button>
        </div>

        <div style={{ marginTop: '32px' }}>
          <h4 className="library-header" style={{ color: 'var(--color-text-muted)', marginBottom: '16px', fontSize: '0.875rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Library
          </h4>
          <nav className="nav-menu">
            <a href="#" className={`nav-item ${activeLectureId === 'current' ? 'active' : ''}`} onClick={handleCurrentUploadClick} aria-current={activeLectureId === 'current' ? 'page' : undefined} title="Current Upload">
              <FileIcon /> <span>Current Upload</span>
            </a>
            {lecturesList.map(file => (
              <a href="#" key={file.id} className={`nav-item ${activeLectureId === file.id ? 'active' : ''}`} onClick={(e) => handlePastUploadClick(file, e)} title={file.title}>
                <FileIcon />
                <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  <div style={{ fontSize: '0.875rem', color: 'var(--color-text-primary)' }}>{file.title}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', fontWeight: 400 }}>
                    {file.created_at ? new Date(file.created_at).toLocaleDateString() : 'Unknown Date'}
                  </div>
                </div>
              </a>
            ))}
          </nav>
        </div>
      </aside>

      {/* Mobile Top Navigation Header */}
      <header className="mobile-header">
        <div className="brand" style={{ fontSize: '1.25rem' }}>
          <div className="brand-icon" style={{ width: '30px', height: '30px', fontSize: '1rem' }}>✓</div>
          LectureCheck
        </div>
        <button 
          className="menu-toggle"
          onClick={() => setIsSidebarOpen(true)}
          aria-label="Open menu"
          aria-expanded={isSidebarOpen}
          aria-controls="sidebar"
        >
          <MenuIcon />
        </button>
      </header>

      {/* Main Dashboard Area */}
      <main className="main-content">
        <div className="page-header animate-up">
          <h1 style={{ marginBottom: '8px' }}>Dashboard</h1>
          <p style={{ color: 'var(--color-text-secondary)', fontSize: '1.125rem' }}>
            Upload a lecture to generate questions and analyze student understanding.
          </p>
        </div>

        {/* Upload Section (visible only when not analyzed) */}
        {uploadState !== 'done' && (
          <div className="card animate-up delay-1" style={{ marginBottom: '48px' }}>
            <div 
              className={`upload-area ${uploadState === 'uploading' ? 'drag-active' : ''}`}
              onClick={handleUpload}
              onKeyDown={handleUploadKeyDown}
              role="button"
              tabIndex={uploadState === 'idle' ? 0 : -1}
              aria-label="Upload lecture slides"
            >
              {uploadState === 'idle' && (
                <>
                  <div className="upload-icon"><UploadIcon /></div>
                  <div>
                    <h3 style={{ marginBottom: '8px' }}>Upload Lecture Slides</h3>
                    <p style={{ color: 'var(--color-text-secondary)', fontSize: '0.875rem' }}>
                      Drag & drop PDF or PPTX files here, or click to browse
                    </p>
                  </div>
                  <button className="btn" style={{ marginTop: '8px' }} tabIndex={-1}>Select File</button>
                </>
              )}

              {uploadState === 'uploading' && (
                <div style={{ width: '100%', maxWidth: '400px', textAlign: 'center' }}>
                  <div className="upload-icon" style={{ margin: '0 auto 16px', background: 'var(--color-bg-secondary)', borderColor: 'var(--color-action-primary)' }}>
                    <span style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--color-text-primary)' }}>{progress}%</span>
                  </div>
                  <h3 style={{ marginBottom: '16px' }}>Analyzing Slides & Generating Questions...</h3>
                  <div className="progress-bar" style={{ background: 'var(--color-border-default)', overflow: 'hidden' }}>
                    <div 
                      className="progress-fill" 
                      style={{ 
                        width: '100%',
                        transform: `scaleX(${progress / 100})`,
                        transformOrigin: 'left',
                        transition: 'transform 0.1s linear',
                        background: 'var(--color-action-primary)'
                      }}
                    ></div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Compact Status Bar (visible only when done) */}
        {uploadState === 'done' && (
          <div className="active-lecture-bar animate-up">
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <div className="lecture-status-dot"></div>
              <div>
                <span style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', display: 'block', textTransform: 'uppercase', fontWeight: 600, letterSpacing: '0.05em', marginBottom: '2px' }}>
                  Active Lecture
                </span>
                <strong style={{ fontSize: '1.05rem', color: 'var(--color-text-heading)', fontWeight: 600 }}>
                  {activeLectureTitle}
                </strong>
              </div>
            </div>
            <button 
              className="btn btn-ghost" 
              onClick={() => {
                if (window.confirm("Are you sure you want to upload new slides? This will clear all currently active student response data.")) {
                  setUploadState('idle');
                  setActiveLectureId('current');
                  setActiveLectureTitle('Neural_Networks_Lec4.pdf');
                }
              }}
            >
              Upload New Slides
            </button>
          </div>
        )}

        {/* Dashboard Content (Visible after upload/simulating data populated) */}
        {uploadState === 'done' && (
          <div className="dashboard-grid animate-up delay-2">
            
            {/* Left Column: AI insights and details */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
              
              {/* AI Insight Panel */}
              <div className="card ai-panel">
                <div className="ai-header">
                  <div className="ai-icon"><SparkleIcon /></div>
                  AI Understanding Analysis
                </div>
                
                <div className="ai-content-grid">
                  {loadingAnalysis ? (
                    <div style={{ padding: '20px', textAlign: 'center', color: 'var(--color-text-secondary)' }}>
                      Loading AI analysis from backend...
                    </div>
                  ) : analysisError ? (
                    <div style={{ padding: '20px', textAlign: 'center', color: 'var(--color-feedback-error)' }}>
                      Failed to load AI Analysis. Make sure the backend is running at localhost:21679. (Error: {analysisError})
                    </div>
                  ) : (
                    <>
                      <div className="ai-summary">
                        <p style={{ color: 'var(--color-text-primary)', fontSize: '1.05rem', lineHeight: 1.6 }}>
                          {analysisData?.overall_summary || 'No overall summary available.'}
                        </p>
                      </div>
                      <div className="ai-recommendations">
                        <h4 style={{ fontSize: '0.875rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--color-text-secondary)', marginBottom: '8px' }}>
                          Recommended Interventions
                        </h4>
                        <ul className="recommendations-list">
                          {analysisData?.critical_review && (
                            <li className="rec-item critical">
                              <span className="rec-badge critical">Critical Review Needed</span>
                              <p style={{ color: 'var(--color-text-primary)', lineHeight: 1.4 }}>
                                {analysisData.critical_review}
                              </p>
                            </li>
                          )}
                          {analysisData?.mastery_achieved && (
                            <li className="rec-item positive">
                              <span className="rec-badge positive">Mastery Achieved</span>
                              <p style={{ color: 'var(--color-text-primary)', lineHeight: 1.4 }}>
                                {analysisData.mastery_achieved}
                              </p>
                            </li>
                          )}
                        </ul>
                      </div>
                    </>
                  )}
                </div>
              </div>

              {/* Per Question Performance (Accordion Breakdown) */}
              <div className="card">
                <h3 style={{ marginBottom: '20px' }}>Per Question Performance</h3>
                
                <div className="question-list">
                  {statsData?.test_suite ? statsData.test_suite.map((item) => {
                    const isExpanded = expandedQuestion === item.question_number;
                    const color = getScoreColor(item.correct_percentage);
                    return (
                      <div 
                        key={item.question_number} 
                        className={`question-card-wrapper ${isExpanded ? 'expanded' : ''}`}
                      >
                        <div 
                          className="question-item" 
                          onClick={() => setExpandedQuestion(isExpanded ? null : item.question_number)}
                          onKeyDown={(e) => handleQuestionKeyDown(e, item.question_number)}
                          style={{ cursor: 'pointer' }}
                          role="button"
                          tabIndex={0}
                          aria-expanded={isExpanded}
                          aria-controls={`q-details-${item.question_number}`}
                        >
                          <div style={{ flex: 1, paddingRight: '24px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                              <span style={{ fontWeight: 600, color: 'var(--color-text-heading)' }}>Q{item.question_number}: {item.topic_tag}</span>
                            </div>
                            <div className="progress-bar">
                              <div 
                                className="progress-fill" 
                                style={{ 
                                  width: '100%',
                                  transform: `scaleX(${item.correct_percentage / 100})`,
                                  transformOrigin: 'left',
                                  background: color
                                }}
                              ></div>
                            </div>
                          </div>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <div style={{ 
                              width: '60px', 
                              textAlign: 'right', 
                              fontWeight: 700, 
                              fontSize: '1.125rem', 
                              color: color
                            }}>
                              {item.correct_percentage}%
                            </div>
                            <span 
                              className={`expand-chevron ${isExpanded ? 'rotated' : ''}`}
                              style={{ display: 'inline-block' }}
                            >
                              ▼
                            </span>
                          </div>
                        </div>
                        
                        <div 
                          id={`q-details-${item.question_number}`}
                          className="question-expanded-details"
                          aria-hidden={!isExpanded}
                        >
                          <div className="expanded-content-inner">
                            <p className="question-text"><strong>Question Text:</strong> {item.question_text}</p>
                            
                            <div className="options-breakdown">
                              <h5 className="options-title">Response Distribution</h5>
                              {item.options && item.options.map((opt, idx) => {
                                return (
                                  <div 
                                    key={idx} 
                                    className={`option-row ${opt.correct ? 'correct' : 'incorrect'}`}
                                  >
                                    <span className="option-badge">
                                      {opt.correct ? '✓' : '•'}
                                    </span>
                                    <span className="option-label">{opt.text}</span>
                                  </div>
                                );
                              })}
                            </div>
                          </div>
                        </div>
                      </div>
                    );
                  }) : <p style={{color: 'var(--color-text-secondary)', padding: '20px'}}>No question data available.</p>}
                </div>
              </div>
            </div>

            {/* Right Column: Key metrics and QR code join widget */}
            <div className="stats-sidebar">
              {/* QR Distribution Card (No "Classes" stage MVP replacement) */}
              <div className="card qr-card animate-up">
                <span style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', textTransform: 'uppercase', fontWeight: 600, letterSpacing: '0.08em' }}>
                  Student Join Link
                </span>
                <div className="qr-wrapper">
                  <QRCodeSVG />
                </div>
                <div>
                  <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--color-text-heading)', fontFamily: 'monospace', letterSpacing: '-0.02em' }}>
                    check.lec/{quizInfo?.quiz_code || '....'}
                  </div>
                  <p style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', marginTop: '4px', lineHeight: 1.3 }}>
                    Display for students to scan & answer.
                  </p>
                </div>
                <button 
                  className="btn btn-ghost" 
                  onClick={() => setIsTheaterMode(true)}
                  style={{ width: '100%', fontSize: '0.8125rem', padding: '6px 12px', marginTop: '4px' }}
                >
                  Project Join Screen
                </button>
              </div>

              <div className="card stat-card">
                <div className="stat-label">Students Responded</div>
                <div className="stat-value">{statsData?.class_summary?.total_students_submitted || 0}</div>
              </div>
              
              <div className="card stat-card">
                <div className="stat-label">Avg. Score</div>
                <div className="stat-value" style={{ color: 'var(--color-feedback-warning)' }}>
                  {statsData?.class_summary?.average_score && statsData?.test_suite?.length
                    ? (statsData.class_summary.average_score / statsData.test_suite.length * 100).toFixed(0) + '%'
                    : '0%'}
                </div>
              </div>

              <div className="card stat-card">
                <div className="stat-label">Completion Rate</div>
                <div className="stat-value">{(statsData?.class_summary?.total_students_submitted > 0 ? 98 : 0)}%</div>
                <div className="stat-trend" style={{ color: 'var(--color-text-muted)' }}>Almost everyone finished</div>
              </div>
            </div>

          </div>
        )}
        
        {/* High-Fidelity Dashboard Skeleton Loader (visible during upload analysis) */}
        {uploadState === 'uploading' && (
          <div className="dashboard-grid animate-up" style={{ opacity: 0.6, pointerEvents: 'none', marginTop: '24px' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
              <div className="skeleton-block" style={{ height: '220px' }}></div>
              <div className="skeleton-block" style={{ height: '320px' }}></div>
            </div>
            <div className="stats-sidebar">
              <div className="skeleton-card" style={{ height: '254px' }}></div> {/* QR card height */}
              <div className="skeleton-card"></div>
              <div className="skeleton-card"></div>
              <div className="skeleton-card"></div>
            </div>
          </div>
        )}

        {/* Faded Skeleton Stats Empty State (visible when idle / no lecture uploaded) */}
        {uploadState === 'idle' && (
          <div className="animate-up delay-2" style={{ marginTop: '24px' }}>
            <div className="empty-state" style={{ marginBottom: '32px' }}>
              <h3 style={{ marginBottom: '8px' }}>Waiting for Lecture Deck</h3>
              <p style={{ maxWidth: '440px', margin: '0 auto', color: 'var(--color-text-secondary)' }}>
                Please drag or select your slides in the upload zone above to enable live question evaluations and dashboard widgets.
              </p>
            </div>
            {/* Same layout skeleton, but lower opacity (0.15) to eliminate layout shift */}
            <div className="dashboard-grid" style={{ opacity: 0.15, pointerEvents: 'none' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
                <div className="skeleton-block" style={{ height: '220px' }}></div>
                <div className="skeleton-block" style={{ height: '320px' }}></div>
              </div>
              <div className="stats-sidebar">
                <div className="skeleton-card" style={{ height: '254px' }}></div>
                <div className="skeleton-card"></div>
                <div className="skeleton-card"></div>
                <div className="skeleton-card"></div>
              </div>
            </div>
          </div>
        )}

      </main>

      {/* Theater Mode Fullscreen Projection Modal */}
      {isTheaterMode && (
        <div className="theater-modal" role="dialog" aria-modal="true" aria-label="Student join details">
          <button 
            className="theater-close-btn"
            onClick={() => setIsTheaterMode(false)}
            aria-label="Close presentation screen"
          >
            <CloseIcon />
          </button>
          
          <span style={{ fontSize: '1rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', fontWeight: 700, letterSpacing: '0.15em' }}>
            Join the Lecture Session
          </span>
          
          <div className="qr-wrapper" style={{ transform: 'scale(1.2)' }}>
            <QRCodeSVG />
          </div>

          <div style={{ textAlign: 'center', marginTop: '16px' }}>
            <div style={{ fontSize: '3rem', fontWeight: 900, fontFamily: 'monospace', letterSpacing: '-0.02em', color: 'var(--color-action-primary)' }}>
              check.lec/{quizInfo?.quiz_code || '....'}
            </div>
            <p style={{ color: 'var(--color-text-muted)', fontSize: '1rem', marginTop: '12px' }}>
              Scan the QR code or go to the link above on your phone to join.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '16px', marginTop: '24px' }}>
            <button className="btn" onClick={copyToClipboard}>
              {copiedLink ? "Link Copied!" : "Copy Join Link"}
            </button>
            <button className="btn btn-ghost" style={{ border: '1px solid rgba(255, 255, 255, 0.2)', color: 'white' }} onClick={() => setIsTheaterMode(false)}>
              Back to Dashboard
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
