# BlenderToDreamteckSplines
An unofficial exporter converting Blender's bezier curves to splines in [Dreamteck Splines](https://assetstore.unity.com/packages/tools/utilities/dreamteck-splines-61926) for Unity.

## How to:
1. Download the addon as a zip.

![image](https://user-images.githubusercontent.com/4378629/188005118-d63f31a9-4ced-4819-b1a9-01253b09c9fb.png)

2. Install the addon in the addons panel of Blender:

![image](https://user-images.githubusercontent.com/4378629/188004695-487b2988-2b41-4d69-9332-2dc7d8ea021d.png)

3. A new option will appear in the export menu. Select your BezierCurve object and click "Export Dreamteck Spline (.csv)". 

![blender_EOXHheBkAo](https://user-images.githubusercontent.com/4378629/188006546-82d55161-32be-47cd-a697-6d1fef13e9cd.png)

![image](https://user-images.githubusercontent.com/4378629/188004531-dfe5625d-e9a4-4e23-8afa-73b23f0a14f0.png)

4. You will be able to import your new bezier curves as csv through Dreamteck's tool panel. [See more in their manual](https://dreamteck.io/page/dreamteck_splines/user_manual.pdf).

![image](https://user-images.githubusercontent.com/4378629/188005424-916da6fa-4922-46e3-9e97-31727736c01f.png)

![image](https://user-images.githubusercontent.com/4378629/188005484-a4f76faa-94ce-483d-9cf0-75e64e180e1c.png)

5. Done! You should see your spline in Unity.

![Unity_e0gwfO2rXy](https://user-images.githubusercontent.com/4378629/188006592-0eece84d-f1ef-4b35-a490-ee4f7e71e738.png)

## Notes

This was developed on Blender 3.2.2. I can't promise it will work on versions before it.

Currently does not support normals or colors. I'm very open to pull requests so if you have a good idea for implementing either please don't be a stranger! Both are disabled by default.

I am not in any way affiliated with Dreamteck.
