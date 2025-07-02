import "../styling/Home.css";

export default function Home() {
  return (
    <div className="home-container">
      <div className="hero-section">
        <h1 className="home-title">MatchNet</h1>
        <p className="home-subtitle">
          Your source for predictive tennis intelligence for men's ATP tennis matches.
        </p>
        <div className="cta-buttons">
          <button className="primary-btn">View Predictions</button>
          <button className="secondary-btn">Explore Data</button>
        </div>
      </div>
      
      <div className="features-section">
        <div className="feature-card">
          <div className="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M9 19c-5 0-9-4-9-9s4-9 9-9 9 4 9 9-4 9-9 9z"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
          </div>
          <h3>AI-Powered Predictions</h3>
          <p>Machine learning models trained on 20+ years of ATP match data to predict match outcomes with high accuracy.</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
          </div>
          <h3>Smart Betting Analysis</h3>
          <p>Calculate expected value across multiple sportsbooks to identify profitable betting opportunities.</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 20V10M12 20V4M6 20v-6"/>
            </svg>
          </div>
          <h3>Comprehensive Stats</h3>
          <p>Deep dive into player statistics, rankings, and historical performance across all surfaces and tournaments.</p>
        </div>
      </div>
      
      <div className="stats-section">
        <div className="stat-item">
          <div className="stat-number">20+</div>
          <div className="stat-label">Years of Data</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">50K+</div>
          <div className="stat-label">Matches Analyzed</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">85%</div>
          <div className="stat-label">Prediction Accuracy</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">6</div>
          <div className="stat-label">Sportsbooks Tracked</div>
        </div>
      </div>
    </div>
  );
}
