import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Home from './pages/home';
import Adduser from './pages/Adduser';

class App extends Component {
  constructor(state){
  super(state)
    this.state ={
      addedNewStudent :false
    }
  }
  NewStudentAdd = (bool) => {
    this.setState({
      addedNewStudent:bool
    })
  }
  render() {
    return (
    <React.Fragment>
      <Home addedNewStudent={this.state.addedNewStudent} NewStudentAdd={this.NewStudentAdd}/>
      <Adduser NewStudentAdd={this.NewStudentAdd} />
    </React.Fragment>
    );
  }
}

export default App;
