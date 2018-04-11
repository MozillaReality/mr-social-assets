# mr-social-assets

Assets and glTF asset pipeline for the Mozilla Social MR team.

## Build Script Setup:

Install [rust](https://www.rust-lang.org/install.html) and [node.js](https://nodejs.org/).

In your terminal run:

```
cargo install gltf_unlit_generator
```

The build script uses [gltf-bundle](https://github.com/MozillaReality/gltf-bundle) to build gltf bundles files and dependencies that are optimized for distribution on the web. Any files in the project ending with `.bundle.config.json` will be used by the build script to generate glTF bundles and their associated files. The output will be placed in the `dist/` folder.

Example `.bundle.config.json` file:

```json
{
  "name": "BotDefault",
  "version": "0.0.1",
  "output": {
    "filePath": "bots"
  },
  "assets": [
    {
      "name": "BotDefault",
      "src": "./BotDefault_Avatar.fbx",
      "components": ["./components.json"]
    }
  ]
}
```

The `name`, `version`, and `assets` properties are required.

`output.filePath` determines the subdirectory to place the bundle and associated files in the `dist/` directory. Files with the same name will be overwritten. This can be useful when assets have textures or binary data in common.

The `asset.src` property can be a `.fbx`, `.gltf`, or `.glb` file. This asset file will have the following build steps applied to it before being placed in the `dist/` folder:

1.  Convert from `.fbx` or `.glb` to `.gltf`. `.fbx`. Conversions are handled by [FBX2glTF](https://github.com/facebookincubator/FBX2glTF).
2.  Generate unlit textures and add the `MOZ_alt_material` extension to any materials in the `.gltf` file using [gltf-unlit-generator](https://github.com/MozillaReality/gltf-unlit-generator).
3.  Add component data using [gltf-component-data](https://github.com/MozillaReality/gltf-component-data) to `gltf.node.extras` using the supplied `asset.components` array. The `components` array can include paths to json files containing component data or JSON objects containing component data.

    Example component.json:

    ```json
    {
      "scenes": {
        "Root Scene": {
          "loop-animation": {
            "clip": "idle_eyes"
          }
        }
      },
      "nodes": {
        "Head": {
          "scale-audio-feedback": ""
        }
      }
    }
    ```

    Example `.bundle.config.json` file:

    ```json
    {
      "name": "BotDefault",
      "version": "0.0.1",
      "output": {
        "filePath": "bots"
      },
      "assets": [
        {
          "name": "BotDefault",
          "src": "./BotDefault_Avatar.fbx",
          "components": [
            "./components.json",
            {
              "nodes": {
                "Head": {
                  "test-component": true
                }
              }
            }
          ]
        }
      ]
    }
    ```

4.  Using [gltf-content-hash](https://github.com/MozillaReality/gltf-content-hash), rename all referenced assets in the glTF to `<contenthash>.<extension>`. This ensures that cached files referenced in the `.gltf` can be updated. Assets shared between multiple `.gltf` files will have the same content hash and will be fetched from cache rather than downloaded again. `.gltf` files will be renamed to `<gltfName>-<contentHash>.gltf` so that you can easily find and preview gltf files, but still get the same cache busting functionality.
5.  Output two final `.bundle.json` files `<bundle.name>.bundle.json` and `<bundle.name>-<bundle.version>-<timestamp>.bundle.json`. The first bundle will always contain the most recent assets. The second will be a version-locked bundle that you can assume is immutable.

## Running the Build Script:

In your terminal `cd` into the `mr-social-assets` directory and run:

```
npm run build
```

Alternatively on Windows you can double-click the `build.bat` script.

## Deploying to S3

Place the `.env` file with AWS/S3 credentials in the `mr-social-assets` folder.

Example `.env`:

```
AWS_ACCESS_KEY=myaccesskey
AWS_SECRET_ACCESS_KEY=mysecret
S3_BUCKET=mybucket
```

In your terminal `cd` into the `mr-social-assets` directory and run:

```
npm run deploy
```

## Setting CORS Settings for your S3 Bucket

Default CORS settings are stored in [cors-config.json](./cors-config.json).

Using the [AWS CLI](https://aws.amazon.com/cli/):

```
cd mr-social-assets
aws s3api put-bucket-cors --bucket <your bucket name> --cors-configuration file://cors-config.json
```

# License

All assets are licensed with the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

Code is licensed with the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/).
