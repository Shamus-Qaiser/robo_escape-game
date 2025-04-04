import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { Container, Nav, Navbar } from 'react-bootstrap';
import Dashboard from './components/dashboard';
import GameInterface from './components/gameInterface';
import ModelTraining from './components/modeltraining';
import SecurityPanel from './components/securitypanel';
import axios from 'axios';
import './App.css';

function App() {
  const [models, setModels] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    fetchModels();
    fetchLeaderboard();
  }, []);

  const fetchModels = async () => {
    const response = await axios.get('http://localhost:5000/api/models');
    setModels(response.data);
  };

  const fetchLeaderboard = async () => {
    const response = await axios.get('http://localhost:5000/api/game/leaderboard');
    setLeaderboard(response.data);
  };

  return (
    <Router>
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container>
          <Navbar.Brand href="/">AI Trainer Platform</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link href="/">Dashboard</Nav.Link>
              <Nav.Link href="/train">Model Training</Nav.Link>
              <Nav.Link href="/game">AI Game</Nav.Link>
              <Nav.Link href="/security">Security</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container className="mt-4">
        <Switch>
          <Route exact path="/">
            <Dashboard models={models} />
          </Route>
          <Route path="/train">
            <ModelTraining onTrain={fetchModels} />
          </Route>
          <Route path="/game">
            <GameInterface leaderboard={leaderboard} />
          </Route>
          <Route path="/security">
            <SecurityPanel />
          </Route>
        </Switch>
      </Container>
    </Router>
  );
}

export default App;