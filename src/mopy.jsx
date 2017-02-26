import React from 'react';
import { Button, ButtonGroup, Glyphicon } from 'react-bootstrap';
import intersperse from './intersperse';
import Mopidy from 'mopidy';
import Progress from './progress';

class CurrentTrack extends React.Component {
  render() {
    if (this.props.track) {
      var artists = this.props.track.artists.map((artist) => <span key={artist.name}>{artist.name}</span>);
      artists = intersperse(artists, ", ");
      return (
        <div>
          <h1>{artists}</h1>
          <h2>{this.props.track.album.name}</h2>
          <h3>{this.props.track.name}</h3>
        </div>
        );
    }
    return (<div />);
  }
}

class Controls extends React.Component {
  constructor(props) {
    super(props);
    this.handlers = this.handlers.bind(this);
  }

  handlers(e) { this.props.handlers(e.target.name); }

  render() {
    return (
      <ButtonGroup>
        <Button bsSize="large" onClick={this.handlers} name="previous"><Glyphicon glyph="step-backward" /></Button>
        <Button bsSize="large" onClick={this.handlers} name="play"    ><Glyphicon glyph="play"          /></Button>
        <Button bsSize="large" onClick={this.handlers} name="pause"   ><Glyphicon glyph="pause"         /></Button>
        <Button bsSize="large" onClick={this.handlers} name="stop"    ><Glyphicon glyph="stop"          /></Button>
        <Button bsSize="large" onClick={this.handlers} name="next"    ><Glyphicon glyph="step-forward"  /></Button>
      </ButtonGroup>
    );
  }
}

class Mopy extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      connected: false,
      track: false,
      length: 100,
      now: 0,
    }
    this.updateTimePosition = this.updateTimePosition.bind(this)
    this.updateCurrentTrack = this.updateCurrentTrack.bind(this)
    this.controlHandlers = this.controlHandlers.bind(this)
  }

  componentDidMount() {
    this.mopidy = new Mopidy({
      webSocketUrl: 'ws://' + this.props.url + ':6680/mopidy/ws/',
      callingConvention: 'by-position-or-by-name'
    });
    this.mopidy.on("state:online", () => {this.setState({connected:true}); this.requestCurrentTrack();});
    this.mopidy.on("state:offline", () => {this.setState({connected:false});});
    this.timerIDct = setInterval(() => {if (this.state.connected) {this.requestCurrentTrack();}}, 1000);
    this.timerIDtp = setInterval(() => {if (this.state.connected) {this.requestTimePosition();}}, 100);
  }


  requestTimePosition() { this.mopidy.playback.getTimePosition().done(this.updateTimePosition); }
  requestCurrentTrack() { this.mopidy.playback.getCurrentTrack().done(this.updateCurrentTrack); }

  updateTimePosition(result) { this.setState({now: result}); }
  updateCurrentTrack(track) { if (track) { this.setState({track: track, length: track.length}); } }

  componentWillUnmount() {
    this.mopidy.close();
    this.mopidy.off();
    this.mopidy = null;
    clearInterval(this.timerIDtp);
    clearInterval(this.timerIDct);
  }

  controlHandlers(command) { if (this.state.connected) { this.mopidy.playback[command](); }}

  render() {
    return (
      <div>
        <CurrentTrack track={this.state.track} />
        <Controls handlers={this.controlHandlers} />
        <Progress max={this.state.length} now={this.state.now} />
      </div>
      );
  }
}

export default Mopy;
