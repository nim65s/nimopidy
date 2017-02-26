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
      <div className="btn-group" role="group">
        <button className="btn btn-default btn-lg" onClick={this.handlers} name="previous"><span className="glyphicon glyphicon-step-backward" /></button>
        <button className="btn btn-default btn-lg" onClick={this.handlers} name="play"    ><span className="glyphicon glyphicon-play"          /></button>
        <button className="btn btn-default btn-lg" onClick={this.handlers} name="pause"   ><span className="glyphicon glyphicon-pause"         /></button>
        <button className="btn btn-default btn-lg" onClick={this.handlers} name="stop"    ><span className="glyphicon glyphicon-stop"          /></button>
        <button className="btn btn-default btn-lg" onClick={this.handlers} name="next"    ><span className="glyphicon glyphicon-step-forward"  /></button>
      </div>
    );
  }
}

class NiMop extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      connected: false,
      track: false,
    }
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
    this.timerID = setInterval(() => {if (this.state.connected) {this.requestCurrentTrack();}}, 1000);
  }

  requestCurrentTrack() { this.mopidy.playback.getCurrentTrack().done(this.updateCurrentTrack); }

  updateCurrentTrack(track) { if (track) { this.setState({track: track}); } }

  componentWillUnmount() {
    this.mopidy.close();
    this.mopidy.off();
    this.mopidy = null;
    clearInterval(this.timerID);
  }

  controlHandlers(command) { if (this.state.connected) { this.mopidy.playback[command](); }}

  render() {
    return (
      <div>
        <CurrentTrack track={this.state.track} />
        <Controls handlers={this.controlHandlers} />
      </div>
      );
  }
}

ReactDOM.render(
  <NiMop url="nausicaa.suginami" />,
  document.getElementById('container')
);


// http://stackoverflow.com/a/23619085/1368502
/* intersperse: Return an array with the separator interspersed between
 * each element of the input array.
 *
 * > _([1,2,3]).intersperse(0)
 * [1,0,2,0,3]
 */
function intersperse(arr, sep) {
  if (arr.length === 0) {
    return [];
  }

  return arr.slice(1).reduce(function(xs, x, i) {
    return xs.concat([sep, x]);
  }, [arr[0]]);
}
