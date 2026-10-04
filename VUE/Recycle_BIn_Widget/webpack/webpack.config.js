const path = require("path");
const { VueLoaderPlugin } = require("vue-loader");
const CopyPlugin = require("copy-webpack-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const webpack = require("webpack");
const TerserPlugin = require("terser-webpack-plugin");
module.exports = {
  entry: "./src/lib/widget-starter.js",
  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "\\\\pu2vwtmcproj03\\webapps\\CR_Widget"),
    publicPath: "",
    assetModuleFilename: "assets/images/[name][ext]",
  },
  mode: "development",
  performance: {
    maxAssetSize: 1000000,
  },
  module: {
    rules: [
      {
        test: /\.(png|jpg|gif)$/i,
        type: "asset/resource",
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        type: "asset/resource",
        generator: {
          filename: "assets/fonts/[name][ext]",
        },
      },
      {
        test: /\.vue$/,
        loader: "vue-loader",
      },
      {
        test: /\.js$/,
        loader: "babel-loader",
        exclude: [/node_modules/, /src\/assets/],
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.md$/i,
        use: "raw-loader",
      },
    ],
  },
  resolve: {
    alias: {
      vue: path.resolve("./node_modules/vue"),
    },
  },
  plugins: [
    new webpack.optimize.LimitChunkCountPlugin({
      maxChunks: 1,
    }),
    new CleanWebpackPlugin(),
    new CopyPlugin({
      patterns: [
        {
          from: "./src/index.html",
          to: "./index.html",
        },
        {
          from: "./src/assets",
          to: "assets",
          globOptions: {
            ignore: ["*.md"],
          },
        },
      ],
    }),
    new VueLoaderPlugin(),
  ],
  optimization: {
    minimizer: [
      new TerserPlugin({
        extractComments: false,
      }),
    ],
  },
};
