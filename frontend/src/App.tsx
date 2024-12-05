import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>C-3PO Assistant from Star Wars</h1>
        <p>Your Personal Protocol Droid from Pedro Victor Veras</p>
      </header>
      <main className="app-main">
        <ChatInterface />
      </main>
    </div>
  );
}

export default App;
