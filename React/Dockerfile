# Webpack build execution
FROM node:8.15.1-alpine AS builder
RUN mkdir react && \
    cd react && \
    yarn init -y && \
    mkdir src public && \
    yarn add react react-dom react-router-dom query-string whatwg-fetch && \
    yarn add webpack webpack-dev-server webpack-cli --dev && \
    yarn add @material-ui/core css-loader style-loader && \
    yarn add @babel/core babel-loader @babel/preset-env @babel/preset-react @babel/cli --dev
COPY ./package.json ./webpack.config.js ./.babelrc /react/
COPY ./src/ /react/src/
WORKDIR /react
RUN yarn build

# webpack-dev-server execution
FROM builder
WORKDIR /react
CMD ["yarn", "start"]
