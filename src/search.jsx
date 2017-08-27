import React from 'react';
import { Glyphicon, Table, Button, FormControl } from 'react-bootstrap';
import './search.css';

class Result extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      added: false,
    }
  }

  add() {
    this.props.mopidy.tracklist.add({uri: this.props.result.uri});
    this.setState({ added: this.props.result.uri });
  }

  render () {
    var length = new Date(this.props.result.length).toISOString().substr(14,5);
    return (
      <tr>
        <td>{this.props.result.name}</td>
        <td>{this.props.result.artists ? this.props.result.artists[0].name : ''}</td>
        <td>{this.props.result.album ? this.props.result.album.name : ''}</td>
        <td>{this.props.uri.split(':')[0]}</td>
        <td>{length}</td>
        <td>
          <Button bsSize="sm" bsStyle={this.state.added == this.props.result.uri ? "success" : ""}
            onClick={this.add.bind(this)} disabled={this.state.adde == this.props.result.uri }>
            <Glyphicon glyph={this.state.added == this.props.result.uri ? "ok" : "plus"} />
          </Button>
        </td>
      </tr>
    );
  }
}

class Search extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      any: '',
      results: [],
      searching: [],
    }
  }

  handleChange(event) {
    this.setState({any: event.target.value});
  }

  handleSubmit(event) {
    if (this.state.any.length > 4) {
      this.setState({searching: <Glyphicon glyph="refresh" className="gly-spin" />});
      this.props.mopidy.library.search({any: [this.state.any]})
        .done(results => this.setState({results: results, searching: []}));
    }
    event.preventDefault();
  }

  render() {
    var results = [];
    if (this.state.results) {
      for (var i = 0; i < this.state.results.length; i++) {
        if (this.state.results[i].tracks) {
          for (var j = 0; j < this.state.results[i].tracks.length; j++) {
            results.push(<Result result={this.state.results[i].tracks[j]} uri={this.state.results[i].uri} mopidy={this.props.mopidy} />);
          }
        }
      }
    }
    return (
      <div>
        <form onSubmit={this.handleSubmit.bind(this)}>
          <FormControl type="text" placeholder="Any Query" value={this.state.value} onChange={this.handleChange.bind(this)} />
        </form>
        {this.state.searching}
        <Table striped condensed hover>
          <thead>
            <tr>
              <th>Title</th>
              <th>Artist</th>
              <th>Album</th>
              <th>Source</th>
              <th>Time</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {results}
          </tbody>
        </Table>
      </div>
      );
  }
}

export default Search;
