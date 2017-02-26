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
      maxVol: 100,
      volume: 100,
      mute: false,
    }
    this.updateTimePosition = this.updateTimePosition.bind(this)
    this.updateCurrentTrack = this.updateCurrentTrack.bind(this)
    this.updateVolume = this.updateVolume.bind(this)
    this.updateMute = this.updateMute.bind(this)
    this.controlHandlers = this.controlHandlers.bind(this)
    this.handleSeek = this.handleSeek.bind(this)
    this.handleVolume = this.handleVolume.bind(this)
  }

  componentDidMount() {
    this.mopidy = new Mopidy({
      webSocketUrl: 'ws://' + this.props.url + ':6680/mopidy/ws/',
      callingConvention: 'by-position-or-by-name'
    });
    this.mopidy.on("state:online", () => {this.setState({connected:true}); this.requestCurrentTrack();});
    this.mopidy.on("state:offline", () => {this.setState({connected:false});});
    this.timerIDtp = setInterval(() => {if (this.state.connected) {this.requestTimePosition();}}, 100);
    this.timerIDct = setInterval(() => {if (this.state.connected) {this.requestCurrentTrack();}}, 1000);
    this.timerIDvm = setInterval(() => {if (this.state.connected) {this.requestVolume();}}, 10000);
  }


  requestTimePosition() { this.mopidy.playback.getTimePosition().done(this.updateTimePosition); }
  requestCurrentTrack() { this.mopidy.playback.getCurrentTrack().done(this.updateCurrentTrack); }
  requestVolume() {
    this.mopidy.mixer.getVolume().done(this.updateVolume);
    this.mopidy.mixer.getMute().done(this.updateMute);
  }

  updateTimePosition(result) { this.setState({now: result}); }
  updateCurrentTrack(track) { if (track) { this.setState({track: track, length: track.length}); } }
  updateVolume(vol) { this.setState({volume: vol}); }
  updateMute(mute) { this.setState({mute: mute}); }

  handleSeek(time) { this.mopidy.playback.seek({'time_position': time}); }
  handleVolume(vol) { console.log(vol); this.mopidy.mixer.setVolume({'volume': vol}); this.updateVolume(vol); }

  componentWillUnmount() {
    this.mopidy.close();
    this.mopidy.off();
    this.mopidy = null;
    clearInterval(this.timerIDtp);
    clearInterval(this.timerIDct);
    clearInterval(this.timerIDvm);
  }

  controlHandlers(command) { if (this.state.connected) { this.mopidy.playback[command](); }}

  render() {
    return (
      <div>
        <CurrentTrack track={this.state.track} />
        <Controls handlers={this.controlHandlers} />
        <Progress max={this.state.maxVol} now={this.state.volume} onSeek={this.handleVolume} />
        <Progress max={this.state.length} now={this.state.now} onSeek={this.handleSeek} />
      </div>
      );
  }
}

export default Mopy;
