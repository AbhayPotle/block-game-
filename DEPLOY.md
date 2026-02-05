# How to Share Your Game

Since this game is built with standard web technologies (HTML, CSS, JavaScript), you can host it for free on many services. Responding to your request, here is the easiest way to get a shareable link.

## Option 1: Netlify Drop (Easiest - Drag & Drop)
**No account required initially, and it takes 30 seconds.**

1.  Locate the `web` folder inside your project directory:
    - Path: `c:\Users\abhay\blocks\web`
2.  Go to **[app.netlify.com/drop](https://app.netlify.com/drop)**.
3.  Drag and drop the entire `web` folder onto the page.
4.  Wait a few seconds for it to upload.
5.  **Done!** Netlify will give you a random URL (e.g., `optimistic-beaver-12345.netlify.app`).
6.  You can copy this link and send it to your friends. They can play it on their computers immediately!

> **Note**: If you want to customize the link name (e.g., `neon-blocks-game`), you will need to create a free Netlify account.

## Option 2: GitHub Pages (If you use Git)
If you put this project on GitHub:
1.  Go to your repository settings.
2.  Scroll down to "Pages".
3.  Select the `web` folder as the source (if possible) or push the `web` folder content to a `gh-pages` branch.
4.  Your game will be live at `yourusername.github.io/repository-name`.

## Important Note
Because the game uses the camera, the hosted link MUST start with `https://`. Both Netlify and GitHub Pages provide this automatically. If you host it yourself elsewhere, ensure SSL is enabled, or the browser will block camera access.
