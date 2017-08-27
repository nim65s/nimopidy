import React from 'react';
import { Glyphicon, Table, Button, FormControl } from 'react-bootstrap';

class Result extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      added: false,
    }
  }

  add() {
    this.props.mopidy.tracklist.add({uri: this.props.result.uri});
    this.setState({ added: true });
  }

  render () {
    var length = new Date(this.props.result.length).toISOString().substr(14,5);
    return (
      <tr>
        <td>{this.props.result.name}</td>
        <td>{this.props.result.artists ? this.props.result.artists[0].name : ''}</td>
        <td>{this.props.result.album ? this.props.result.album.name : ''}</td>
        <td>{length}</td>
        <td>
          <Button bsSize="sm" bsStyle={this.state.added ? "success" : ""} onClick={this.add.bind(this)} disabled={this.state.added}>
            <Glyphicon glyph={this.state.added ? "ok" : "plus"} />
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
      results: [],
    }
  }

  handleChange(e) {
    if (e.target.value.length > 4) {
      this.props.mopidy.library.search({any: [e.target.value], uris: ['spotify:']})
        .done(results => this.setState({results: results[0].tracks}));
    }
  }

  render() {
    var results = [];
    if (this.state.results) {
      for (var i = 0; i < this.state.results.length; i++) {
        results.push(<Result result={this.state.results[i]} mopidy={this.props.mopidy} />);
      }
    }
    return (
      <div>
        <form>
          <FormControl type="text" onChange={this.handleChange.bind(this)} />
        </form>
        <Table striped condensed hover>
          <thead>
            <tr>
              <th>Title</th>
              <th>Artist</th>
              <th>Album</th>
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
