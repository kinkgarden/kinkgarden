var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    context: __dirname,

    devtool: process.env.NODE_ENV === 'development' && "inline-source-map",

    entry: './assets/index',

    output: {
        path: path.resolve('./static/editor/'),
        filename: "[name]-[hash].js",
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new MiniCssExtractPlugin({filename: "[name]-[hash].css"}),
    ],

    resolve: {
        // see below for an explanation
        mainFields: ['svelte', 'browser', 'module', 'main']
    },
    module: {
        rules: [
            {
                test: /\.(html|svelte)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'svelte-loader',
                    options: {
                        emitCss: true,
                    }
                }
            },
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader'],
            }
        ]
    },
};
