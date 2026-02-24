import { useState, useEffect } from 'react';
import { Users, Building2, DollarSign, MapPin, Globe, TrendingUp, Home, Briefcase, Train, Film, Landmark, AlertTriangle } from 'lucide-react';
import Card from '../components/Card';
import './Pages.css';

const CityOverview = () => {
  const [activeSection, setActiveSection] = useState('overview');

  const StatCard = ({ icon: Icon, label, value, sublabel, color }) => (
    <div className="stat-card" style={{ borderLeftColor: color }}>
      <div className="stat-icon" style={{ color }}>
        <Icon size={24} />
      </div>
      <div className="stat-content">
        <div className="stat-label">{label}</div>
        <div className="stat-value">{value}</div>
        {sublabel && <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '0.25rem' }}>{sublabel}</div>}
      </div>
    </div>
  );

  const InfoSection = ({ title, icon: Icon, children }) => (
    <div style={{
      padding: '1.5rem',
      background: '#1e293b',
      borderRadius: '0.75rem',
      marginBottom: '1rem',
      borderLeft: '4px solid #3b82f6'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
        <Icon size={24} color="#3b82f6" />
        <h3 style={{ fontSize: '1.125rem', fontWeight: 'bold', color: 'white', margin: 0 }}>{title}</h3>
      </div>
      <div style={{ fontSize: '0.875rem', color: '#cbd5e1', lineHeight: '1.6' }}>
        {children}
      </div>
    </div>
  );

  const landmarkImages = [
    {
      url: 'https://images.unsplash.com/photo-1566552881560-0be862a7c445?w=800',
      title: 'Gateway of India',
      desc: 'Iconic monument overlooking the Arabian Sea'
    },
    {
      url: 'https://images.unsplash.com/photo-1595658658481-d53d3f999875?w=800',
      title: 'Marine Drive',
      desc: "The Queen's Necklace at sunset"
    },
    {
      url: 'https://images.unsplash.com/photo-1567157577867-05ccb1388e66?w=800',
      title: 'CST Terminus',
      desc: 'UNESCO World Heritage railway station'
    }
  ];

  return (
    <div className="page">
      {/* Hero Section with Image */}
      <div style={{
        position: 'relative',
        height: '300px',
        borderRadius: '1rem',
        overflow: 'hidden',
        marginBottom: '2rem',
        background: 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)'
      }}>
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage: 'url(https://images.unsplash.com/photo-1566552881560-0be862a7c445?w=1200)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          opacity: 0.3
        }} />
        <div style={{
          position: 'relative',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          textAlign: 'center',
          padding: '2rem',
          background: 'linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.6))'
        }}>
          <h1 style={{ 
            fontSize: '3rem', 
            fontWeight: 'bold', 
            color: 'white', 
            marginBottom: '1rem',
            textShadow: '2px 2px 4px rgba(0,0,0,0.5)'
          }}>
            🏙️ Mumbai - City of Dreams
          </h1>
          <p style={{ 
            fontSize: '1.25rem', 
            color: '#e0e7ff', 
            marginBottom: '1rem',
            textShadow: '1px 1px 2px rgba(0,0,0,0.5)'
          }}>
            India's Financial Capital & Gateway to the Nation
          </p>
          <div style={{ 
            display: 'flex',
            gap: '2rem',
            marginTop: '1rem'
          }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#60a5fa' }}>12.4M</div>
              <div style={{ fontSize: '0.875rem', color: '#cbd5e1' }}>Population</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#34d399' }}>$277B</div>
              <div style={{ fontSize: '0.875rem', color: '#cbd5e1' }}>GDP</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#fbbf24' }}>18.96°N</div>
              <div style={{ fontSize: '0.875rem', color: '#cbd5e1' }}>Latitude</div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div style={{ 
        display: 'flex', 
        gap: '0.5rem', 
        marginBottom: '1.5rem',
        flexWrap: 'wrap'
      }}>
        {[
          { id: 'overview', label: 'Overview', icon: MapPin },
          { id: 'economy', label: 'Economy', icon: DollarSign },
          { id: 'culture', label: 'Culture', icon: Film },
          { id: 'challenges', label: 'Challenges', icon: AlertTriangle }
        ].map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setActiveSection(id)}
            style={{
              padding: '0.5rem 1rem',
              background: activeSection === id ? '#3b82f6' : '#1e293b',
              color: 'white',
              border: 'none',
              borderRadius: '0.5rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              fontSize: '0.875rem',
              transition: 'all 0.3s'
            }}
          >
            <Icon size={16} />
            {label}
          </button>
        ))}
      </div>

      {/* Key Statistics */}
      <div className="stats-grid">
        <StatCard
          icon={Users}
          label="Population"
          value="12.4M"
          sublabel="City Proper (2023)"
          color="#3b82f6"
        />
        <StatCard
          icon={Globe}
          label="Metro Population"
          value="23M+"
          sublabel="Metropolitan Region"
          color="#8b5cf6"
        />
        <StatCard
          icon={DollarSign}
          label="GDP"
          value="$277B"
          sublabel="Metropolitan Area"
          color="#10b981"
        />
        <StatCard
          icon={TrendingUp}
          label="National GDP"
          value="6.16%"
          sublabel="Contribution to India"
          color="#f59e0b"
        />
      </div>

      {/* Content Sections */}
      {activeSection === 'overview' && (
        <div>
          {/* Image Gallery */}
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '1rem',
            marginBottom: '2rem'
          }}>
            {landmarkImages.map((image, idx) => (
              <div key={idx} style={{
                position: 'relative',
                height: '200px',
                borderRadius: '0.75rem',
                overflow: 'hidden',
                cursor: 'pointer',
                transition: 'transform 0.3s',
                boxShadow: '0 4px 6px rgba(0,0,0,0.3)'
              }}
              onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
              onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
              >
                <img 
                  src={image.url} 
                  alt={image.title}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover'
                  }}
                />
                <div style={{
                  position: 'absolute',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  padding: '1rem',
                  background: 'linear-gradient(to top, rgba(0,0,0,0.8), transparent)',
                  color: 'white'
                }}>
                  <div style={{ fontSize: '1rem', fontWeight: 'bold', marginBottom: '0.25rem' }}>
                    {image.title}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>
                    {image.desc}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <InfoSection title="Geography & History" icon={MapPin}>
            <p style={{ marginBottom: '1rem' }}>
              Mumbai evolved from a cluster of <strong>seven islands</strong>—Isle of Bombay, Parel, Mazagaon, 
              Mahim, Colaba, Worli, and Old Woman's Island—connected through centuries of land reclamation, 
              notably the <strong>Hornby Vellard project</strong> (completed in 1845).
            </p>
            <p style={{ marginBottom: '1rem' }}>
              Today, it occupies a narrow peninsula on <strong>Salsette Island</strong>, bordered by the 
              Arabian Sea to the west, Thane Creek to the east, and Vasai Creek to the north. The city sits 
              at an average elevation of <strong>14 meters (46 ft)</strong>.
            </p>
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '1rem',
              marginTop: '1rem',
              padding: '1rem',
              background: '#0f172a',
              borderRadius: '0.5rem'
            }}>
              <div>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Former Name</div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'white' }}>Bombay</div>
              </div>
              <div>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Name Changed</div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'white' }}>1995</div>
              </div>
              <div>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Elevation</div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'white' }}>14m (46 ft)</div>
              </div>
              <div>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Seismic Zone</div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: '#f59e0b' }}>Zone III</div>
              </div>
            </div>
          </InfoSection>

          <div className="grid-2">
            <Card title="🏛️ Iconic Landmarks">
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {[
                  { 
                    name: 'Gateway of India', 
                    type: 'Monument', 
                    status: 'UNESCO Heritage',
                    img: 'https://images.unsplash.com/photo-1566552881560-0be862a7c445?w=400'
                  },
                  { 
                    name: 'CST Terminus', 
                    type: 'Railway Station', 
                    status: 'UNESCO Heritage',
                    img: 'https://images.unsplash.com/photo-1567157577867-05ccb1388e66?w=400'
                  },
                  { 
                    name: 'Marine Drive', 
                    type: 'Promenade', 
                    status: "Queen's Necklace",
                    img: 'https://images.unsplash.com/photo-1595658658481-d53d3f999875?w=400'
                  },
                  { 
                    name: 'Elephanta Caves', 
                    type: 'Archaeological', 
                    status: 'UNESCO Heritage',
                    img: 'https://images.unsplash.com/photo-1587474260584-136574528ed5?w=400'
                  }
                ].map((landmark, idx) => (
                  <div key={idx} style={{
                    padding: '0.75rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    borderLeft: '3px solid #3b82f6',
                    display: 'flex',
                    gap: '1rem',
                    alignItems: 'center'
                  }}>
                    <img 
                      src={landmark.img}
                      alt={landmark.name}
                      style={{
                        width: '80px',
                        height: '60px',
                        objectFit: 'cover',
                        borderRadius: '0.5rem'
                      }}
                    />
                    <div style={{ flex: 1 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                          <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                            {landmark.name}
                          </div>
                          <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                            {landmark.type}
                          </div>
                        </div>
                        <div style={{
                          padding: '0.25rem 0.5rem',
                          background: '#1e3a8a',
                          borderRadius: '0.25rem',
                          fontSize: '0.625rem',
                          color: '#60a5fa'
                        }}>
                          {landmark.status}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            <Card title="🚇 Transport Network">
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {[
                  { name: 'Mumbai Suburban Railway', stat: "World's Busiest", icon: '🚆' },
                  { name: 'Mumbai Metro', stat: 'Expanding Network', icon: '🚇' },
                  { name: 'Mumbai Monorail', stat: 'Elevated Transit', icon: '🚝' },
                  { name: 'CSMIA Airport', stat: 'International Hub', icon: '✈️' },
                  { name: 'Mumbai Port', stat: '70% Maritime Trade', icon: '🚢' }
                ].map((transport, idx) => (
                  <div key={idx} style={{
                    padding: '0.75rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '1rem'
                  }}>
                    <div style={{ fontSize: '1.5rem' }}>{transport.icon}</div>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                        {transport.name}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                        {transport.stat}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </div>
      )}

      {activeSection === 'economy' && (
        <div>
          {/* Economic Skyline Banner */}
          <div style={{
            position: 'relative',
            height: '200px',
            borderRadius: '0.75rem',
            overflow: 'hidden',
            marginBottom: '2rem',
            boxShadow: '0 4px 6px rgba(0,0,0,0.3)'
          }}>
            <img 
              src="https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=1200"
              alt="Mumbai Skyline"
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover'
              }}
            />
            <div style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'linear-gradient(to right, rgba(0,0,0,0.7), rgba(0,0,0,0.3))',
              display: 'flex',
              alignItems: 'center',
              padding: '2rem'
            }}>
              <div>
                <h2 style={{ fontSize: '2rem', fontWeight: 'bold', color: 'white', marginBottom: '0.5rem' }}>
                  💼 Financial Capital of India
                </h2>
                <p style={{ fontSize: '1rem', color: '#cbd5e1' }}>
                  Home to BSE, NSE, RBI, and India's largest corporations
                </p>
              </div>
            </div>
          </div>

          <InfoSection title="Financial Capital of India" icon={DollarSign}>
            <p style={{ marginBottom: '1rem' }}>
              Mumbai is India's <strong>financial capital</strong>, housing the Bombay Stock Exchange (BSE), 
              the National Stock Exchange (NSE), the Reserve Bank of India (RBI), and headquarters of major 
              Indian conglomerates like <strong>Tata, Reliance, and Aditya Birla</strong>.
            </p>
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
              gap: '1rem',
              marginTop: '1rem'
            }}>
              {[
                { label: 'Industrial Output', value: '25%', desc: 'of India' },
                { label: 'Maritime Trade', value: '70%', desc: 'of India' },
                { label: 'National GDP', value: '6.16%', desc: 'Contribution' },
                { label: 'Metro GDP', value: '$277B', desc: 'Total' }
              ].map((stat, idx) => (
                <div key={idx} style={{
                  padding: '1rem',
                  background: '#1e293b',
                  borderRadius: '0.5rem',
                  textAlign: 'center',
                  borderTop: '3px solid #10b981'
                }}>
                  <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#10b981' }}>
                    {stat.value}
                  </div>
                  <div style={{ fontSize: '0.875rem', color: 'white', marginTop: '0.25rem' }}>
                    {stat.label}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.25rem' }}>
                    {stat.desc}
                  </div>
                </div>
              ))}
            </div>
          </InfoSection>

          <div className="grid-2">
            <Card title="🏢 Major Corporations">
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {[
                  { name: 'Tata Group', sector: 'Conglomerate', hq: 'Bombay House' },
                  { name: 'Reliance Industries', sector: 'Energy & Retail', hq: 'Maker Chambers' },
                  { name: 'Aditya Birla Group', sector: 'Conglomerate', hq: 'Indian Rayon' },
                  { name: 'State Bank of India', sector: 'Banking', hq: 'Nariman Point' },
                  { name: 'HDFC Bank', sector: 'Banking', hq: 'BKC' },
                  { name: 'ICICI Bank', sector: 'Banking', hq: 'BKC' }
                ].map((corp, idx) => (
                  <div key={idx} style={{
                    padding: '0.75rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}>
                    <div>
                      <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                        {corp.name}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                        {corp.sector}
                      </div>
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
                      {corp.hq}
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            <Card title="📊 Economic Indicators">
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {[
                  { label: 'Billionaires', value: 'Highest in Asia', color: '#f59e0b' },
                  { label: 'World City Rank', value: 'Alpha City (2008)', color: '#3b82f6' },
                  { label: 'Stock Exchanges', value: 'BSE & NSE', color: '#10b981' },
                  { label: 'Port Traffic', value: '70% of India', color: '#8b5cf6' }
                ].map((indicator, idx) => (
                  <div key={idx} style={{
                    padding: '1rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    borderLeft: `4px solid ${indicator.color}`
                  }}>
                    <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.25rem' }}>
                      {indicator.label}
                    </div>
                    <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'white' }}>
                      {indicator.value}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </div>
      )}

      {activeSection === 'culture' && (
        <div>
          {/* Bollywood Banner */}
          <div style={{
            position: 'relative',
            height: '200px',
            borderRadius: '0.75rem',
            overflow: 'hidden',
            marginBottom: '2rem',
            background: 'linear-gradient(135deg, #7c3aed 0%, #ec4899 100%)',
            boxShadow: '0 4px 6px rgba(0,0,0,0.3)'
          }}>
            <div style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundImage: 'url(https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=1200)',
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              opacity: 0.3
            }} />
            <div style={{
              position: 'relative',
              height: '100%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              textAlign: 'center',
              padding: '2rem'
            }}>
              <div>
                <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>🎬</div>
                <h2 style={{ fontSize: '2rem', fontWeight: 'bold', color: 'white', marginBottom: '0.5rem' }}>
                  Bollywood Capital
                </h2>
                <p style={{ fontSize: '1rem', color: '#fce7f3' }}>
                  1000+ films produced annually • World's largest film industry
                </p>
              </div>
            </div>
          </div>

          <InfoSection title="Cultural Hub & Bollywood" icon={Film}>
            <p style={{ marginBottom: '1rem' }}>
              Mumbai is the epicenter of <strong>Bollywood</strong>, India's largest film industry, and a 
              global hub for music, fashion, and arts. The city is renowned for its diverse street food, 
              vibrant festivals, and multicultural population.
            </p>
            <p>
              Residents are called <strong>Mumbaikars</strong> (Marathi: मुंबईकर). The official languages 
              are Marathi and English. The city is a melting pot of religions, languages, and cultures, with 
              significant communities of Hindus, Muslims, Christians, Parsis, and others.
            </p>
          </InfoSection>

          <div className="grid-2">
            <Card title="🎬 Bollywood & Entertainment">
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f59e0b', marginBottom: '0.5rem' }}>
                  🎥 Film City
                </div>
                <p style={{ fontSize: '0.875rem', color: '#cbd5e1', lineHeight: '1.6' }}>
                  Mumbai produces over 1,000 films annually, making it the world's largest film production 
                  center. Major studios include Film City, Mehboob Studios, and Yash Raj Studios.
                </p>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {[
                  { item: 'Annual Film Production', value: '1000+ films' },
                  { item: 'Music Industry', value: 'Global Hub' },
                  { item: 'Fashion Weeks', value: 'Lakmé Fashion Week' },
                  { item: 'Art Galleries', value: 'Jehangir, NGMA' }
                ].map((item, idx) => (
                  <div key={idx} style={{
                    padding: '0.75rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    display: 'flex',
                    justifyContent: 'space-between'
                  }}>
                    <span style={{ fontSize: '0.875rem', color: '#cbd5e1' }}>{item.item}</span>
                    <span style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>{item.value}</span>
                  </div>
                ))}
              </div>
            </Card>

            <Card title="🍛 Street Food & Festivals">
              <div style={{ marginBottom: '1rem' }}>
                <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🎉</div>
                <p style={{ fontSize: '0.875rem', color: '#cbd5e1', lineHeight: '1.6', marginBottom: '1rem' }}>
                  Mumbai's street food culture is legendary - from vada pav to pav bhaji, bhel puri to 
                  sev puri. The city celebrates all major festivals with equal enthusiasm.
                </p>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                {[
                  '🥟 Vada Pav',
                  '🍲 Pav Bhaji',
                  '🥗 Bhel Puri',
                  '🌮 Sev Puri',
                  '🍢 Kebabs',
                  '🍰 Irani Chai'
                ].map((food, idx) => (
                  <div key={idx} style={{
                    padding: '0.5rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    textAlign: 'center',
                    fontSize: '0.875rem',
                    color: 'white'
                  }}>
                    {food}
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </div>
      )}

      {activeSection === 'challenges' && (
        <div>
          {/* Challenges Banner */}
          <div style={{
            position: 'relative',
            height: '200px',
            borderRadius: '0.75rem',
            overflow: 'hidden',
            marginBottom: '2rem',
            boxShadow: '0 4px 6px rgba(0,0,0,0.3)'
          }}>
            <img 
              src="https://images.unsplash.com/photo-1547683905-f686c993aae5?w=1200"
              alt="Mumbai Monsoon"
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover'
              }}
            />
            <div style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'linear-gradient(to bottom, rgba(0,0,0,0.5), rgba(0,0,0,0.8))',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              textAlign: 'center',
              padding: '2rem'
            }}>
              <div>
                <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>⚠️</div>
                <h2 style={{ fontSize: '2rem', fontWeight: 'bold', color: 'white', marginBottom: '0.5rem' }}>
                  Urban Challenges
                </h2>
                <p style={{ fontSize: '1rem', color: '#fca5a5' }}>
                  Addressing inequality, flooding, and infrastructure strain
                </p>
              </div>
            </div>
          </div>

          <InfoSection title="Urban Challenges" icon={AlertTriangle}>
            <p style={{ marginBottom: '1rem' }}>
              Despite its prosperity, Mumbai faces stark contrasts: <strong>extreme social inequality</strong>, 
              overcrowding, and infrastructure strain. While high-end business districts like Nariman Point 
              and Bandra-Kurla Complex (BKC) thrive, vast slums—including <strong>Dharavi, Asia's largest</strong>—house millions.
            </p>
            <p>
              The city is <strong>seismically active (Seismic Zone III)</strong>, and climate vulnerability 
              is increasing due to rising sea levels and monsoon flooding.
            </p>
          </InfoSection>

          <div className="grid-2">
            <Card title="⚠️ Key Challenges">
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {[
                  { 
                    challenge: 'Social Inequality', 
                    severity: 'HIGH',
                    desc: 'Stark contrast between wealth and poverty',
                    color: '#ef4444'
                  },
                  { 
                    challenge: 'Overcrowding', 
                    severity: 'HIGH',
                    desc: '12.4M people in limited space',
                    color: '#ef4444'
                  },
                  { 
                    challenge: 'Monsoon Flooding', 
                    severity: 'HIGH',
                    desc: 'Annual flooding during monsoon season',
                    color: '#f59e0b'
                  },
                  { 
                    challenge: 'Infrastructure Strain', 
                    severity: 'MEDIUM',
                    desc: 'Aging infrastructure under pressure',
                    color: '#f59e0b'
                  },
                  { 
                    challenge: 'Climate Vulnerability', 
                    severity: 'MEDIUM',
                    desc: 'Rising sea levels threaten coastal areas',
                    color: '#f59e0b'
                  },
                  { 
                    challenge: 'Seismic Risk', 
                    severity: 'MEDIUM',
                    desc: 'Located in Seismic Zone III',
                    color: '#3b82f6'
                  }
                ].map((item, idx) => (
                  <div key={idx} style={{
                    padding: '1rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    borderLeft: `4px solid ${item.color}`
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                      <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                        {item.challenge}
                      </div>
                      <div style={{
                        padding: '0.125rem 0.5rem',
                        background: item.color === '#ef4444' ? '#7f1d1d' : item.color === '#f59e0b' ? '#78350f' : '#1e3a8a',
                        borderRadius: '0.25rem',
                        fontSize: '0.625rem',
                        fontWeight: 'bold',
                        color: item.color
                      }}>
                        {item.severity}
                      </div>
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                      {item.desc}
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            <Card title="🏘️ Slum Areas">
              <div style={{ marginBottom: '1rem', padding: '1rem', background: '#78350f', borderRadius: '0.5rem', borderLeft: '4px solid #f59e0b' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#fbbf24', marginBottom: '0.5rem' }}>
                  Dharavi
                </div>
                <div style={{ fontSize: '0.875rem', color: '#fde68a', marginBottom: '0.5rem' }}>
                  Asia's Largest Slum
                </div>
                <div style={{ fontSize: '0.75rem', color: '#fef3c7', lineHeight: '1.6' }}>
                  Home to nearly 1 million people in just 2.1 sq km. Despite challenges, it's a thriving 
                  economic hub with small-scale industries generating over $1 billion annually.
                </div>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {[
                  { area: 'Dharavi', population: '~1M', size: '2.1 km²' },
                  { area: 'Mankhurd', population: '~500K', size: '1.5 km²' },
                  { area: 'Govandi', population: '~400K', size: '1.2 km²' }
                ].map((slum, idx) => (
                  <div key={idx} style={{
                    padding: '0.75rem',
                    background: '#1e293b',
                    borderRadius: '0.5rem',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}>
                    <div style={{ fontSize: '0.875rem', fontWeight: 'bold', color: 'white' }}>
                      {slum.area}
                    </div>
                    <div style={{ display: 'flex', gap: '1rem', fontSize: '0.75rem', color: '#94a3b8' }}>
                      <span>{slum.population}</span>
                      <span>{slum.size}</span>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};

export default CityOverview;
