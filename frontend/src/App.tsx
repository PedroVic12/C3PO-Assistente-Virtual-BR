import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>C-3PO Assistant</h1>
        <p>Your Personal Protocol Droid</p>
      </header>
      <main className="app-main">
        <ChatInterface />
      </main>
    </div>
  );
}

export default App;
