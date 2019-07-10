module.exports = {
  entry: {
    app: "./src/index.js",
    fetch: "./src/api.js"
   },
  output: {
    path: __dirname + '/public/js',
    filename: "[name].js"
  },
  devServer: {
    contentBase: __dirname + '/public',
    port: 3000,
    publicPath: '/js/',
    disableHostCheck: true,
    watchContentBase: true,
    watchOptions: {
      poll: 1000
    },
    hot: true,
    host: '0.0.0.0'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader'
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              modules: true
            }
          }
        ]
      },
      {
        test: /\.svg$/,
        loader: 'svg-inline-loader'
      }
    ]
  },
  mode: 'none'
};
