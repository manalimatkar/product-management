// In-preview commenting widget.
//
// Adds a "Comment" button next to every ID-only heading (BR-006, DEC-002,
// ...) that comment-map.json (generate_comment_map.py) knows a source
// line for. "Post" calls GitHub's REST API directly from the browser --
// POST /repos/{repo}/pulls/{pr}/comments -- to create a real inline PR
// review comment, using the reviewer's own token (below). This assumes
// api.github.com's CORS policy allows an authenticated browser POST from
// an arbitrary origin (GitHub has supported this for a few years) --
// genuinely unverified until tested against a real PR; if it turns out
// CORS blocks this, the fetch will reject and the error path (below)
// surfaces that instead of failing silently.
//
// Hides itself entirely when there's no PR to comment on (main-site
// build, where comment-map.json's commit_sha/pr_number/repo are null)
// or when the current page has no ID headings at all (e.g. the
// generated home/relationships pages).
//
// Token handling: a fine-grained GitHub Personal Access Token, scoped by
// the reviewer to just this repository's Pull Requests, pasted once and
// kept only in this browser's localStorage -- never sent anywhere but
// api.github.com. This is a real, deliberate tradeoff worth stating
// plainly: a token sitting in localStorage is more exposed than a normal
// OAuth session (any script that ever runs on this origin can read it).
// Acceptable for a small, reviewer-only preview site with no other
// third-party script on the page today; revisit if that ever changes.

(function () {
  "use strict";

  var TOKEN_KEY = "docs-preview-github-token";

  function getToken() {
    try {
      return localStorage.getItem(TOKEN_KEY) || "";
    } catch (e) {
      return ""; // private browsing / storage blocked -- treat as not connected
    }
  }

  function setToken(token) {
    try {
      localStorage.setItem(TOKEN_KEY, token);
    } catch (e) {
      console.warn("[comment-widget] could not save token:", e);
    }
  }

  function clearToken() {
    try {
      localStorage.removeItem(TOKEN_KEY);
    } catch (e) {}
  }

  function buildConnectionBadge() {
    var badge = document.createElement("div");
    badge.className = "comment-widget-badge";

    function render() {
      badge.innerHTML = "";
      if (getToken()) {
        var status = document.createElement("span");
        status.className = "comment-widget-badge-status connected";
        status.textContent = "GitHub connected";
        var disconnect = document.createElement("button");
        disconnect.type = "button";
        disconnect.className = "comment-widget-badge-link";
        disconnect.textContent = "Disconnect";
        disconnect.addEventListener("click", function () {
          clearToken();
          render();
        });
        badge.appendChild(status);
        badge.appendChild(disconnect);
      } else {
        var connect = document.createElement("button");
        connect.type = "button";
        connect.className = "comment-widget-badge-link";
        connect.textContent = "Connect GitHub to comment";
        connect.addEventListener("click", function () {
          promptForToken(render);
        });
        badge.appendChild(connect);
      }
    }

    render();
    return badge;
  }

  function promptForToken(onDone) {
    var overlay = document.createElement("div");
    overlay.className = "comment-widget-modal-overlay";

    var modal = document.createElement("div");
    modal.className = "comment-widget-modal";
    modal.innerHTML =
      '<h3>Connect GitHub</h3>' +
      '<p>Paste a fine-grained Personal Access Token scoped to <strong>this repository\'s Pull Requests (read &amp; write)</strong>. ' +
      'Create one at <code>github.com/settings/personal-access-tokens/new</code>. ' +
      "Stored only in this browser -- never sent anywhere but github.com.</p>";

    var input = document.createElement("input");
    input.type = "password";
    input.placeholder = "github_pat_…";
    input.className = "comment-widget-modal-input";

    var saveBtn = document.createElement("button");
    saveBtn.type = "button";
    saveBtn.className = "comment-widget-post";
    saveBtn.textContent = "Save";
    saveBtn.addEventListener("click", function () {
      var value = input.value.trim();
      if (!value) return;
      setToken(value);
      document.body.removeChild(overlay);
      onDone();
    });

    var cancelBtn = document.createElement("button");
    cancelBtn.type = "button";
    cancelBtn.className = "comment-widget-cancel";
    cancelBtn.textContent = "Cancel";
    cancelBtn.addEventListener("click", function () {
      document.body.removeChild(overlay);
    });

    var actions = document.createElement("div");
    actions.className = "comment-widget-actions";
    actions.appendChild(saveBtn);
    actions.appendChild(cancelBtn);

    modal.appendChild(input);
    modal.appendChild(actions);
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    input.focus();
  }

  function init() {
    var body = document.body;
    var mapUrl = body.dataset.commentMapUrl;
    var sourceFile = body.dataset.sourceFile;
    if (!mapUrl || !sourceFile) return;

    fetch(mapUrl)
      .then(function (r) {
        if (!r.ok) throw new Error("comment-map.json fetch failed: " + r.status);
        return r.json();
      })
      .then(function (data) {
        if (!data.commit_sha || !data.pr_number || !data.repo) {
          // No PR context -- this is the main site, not a PR preview. Nothing to comment on.
          return;
        }
        document.body.appendChild(buildConnectionBadge());

        var idLines = data.files[sourceFile];
        if (!idLines) return; // this page has no ID headings (generated pages, etc.)

        Object.keys(idLines).forEach(function (id) {
          var line = idLines[id];
          var heading = document.getElementById(id.toLowerCase());
          if (!heading) return; // map and rendered page disagree -- skip, don't break the page
          attachCommentButton(heading, {
            repo: data.repo,
            commitSha: data.commit_sha,
            prNumber: data.pr_number,
            path: sourceFile,
            line: line,
            id: id,
          });
        });
      })
      .catch(function (err) {
        console.warn("[comment-widget] disabled:", err);
      });
  }

  function attachCommentButton(heading, target) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "comment-widget-button";
    btn.textContent = "💬 Comment";
    btn.setAttribute("aria-label", "Comment on " + target.id);

    var box = null; // created lazily, one per heading

    btn.addEventListener("click", function () {
      if (box) {
        box.remove();
        box = null;
        return;
      }
      box = buildCommentBox(target, function () {
        box.remove();
        box = null;
      });
      heading.insertAdjacentElement("afterend", box);
      box.querySelector("textarea").focus();
    });

    heading.insertAdjacentElement("afterend", wrapButton(btn));
  }

  function wrapButton(btn) {
    var wrap = document.createElement("div");
    wrap.className = "comment-widget-button-row";
    wrap.appendChild(btn);
    return wrap;
  }

  function postComment(target, body) {
    var url =
      "https://api.github.com/repos/" + target.repo + "/pulls/" + target.prNumber + "/comments";
    return fetch(url, {
      method: "POST",
      headers: {
        Authorization: "Bearer " + getToken(),
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        body: body,
        commit_id: target.commitSha,
        path: target.path,
        line: target.line,
        side: "RIGHT",
      }),
    }).then(function (r) {
      if (!r.ok) {
        return r.json().catch(function () {
          return {};
        }).then(function (err) {
          throw new Error((err && err.message) || "GitHub API error " + r.status);
        });
      }
      return r.json();
    });
  }

  function buildCommentBox(target, onClose) {
    var box = document.createElement("div");
    box.className = "comment-widget-box";

    var textarea = document.createElement("textarea");
    textarea.placeholder = "Leave a comment on " + target.id + "…";
    textarea.rows = 3;

    var status = document.createElement("div");
    status.className = "comment-widget-status";

    var postBtn = document.createElement("button");
    postBtn.type = "button";
    postBtn.className = "comment-widget-post";
    postBtn.textContent = "Post";
    postBtn.addEventListener("click", function () {
      var token = getToken();
      if (!token) {
        promptForToken(function () {
          postBtn.click(); // retry the post now that a token exists
        });
        return;
      }
      var body = textarea.value.trim();
      if (!body) return;

      postBtn.disabled = true;
      postBtn.textContent = "Posting…";
      status.className = "comment-widget-status";
      status.textContent = "";

      postComment(target, body)
        .then(function (comment) {
          status.className = "comment-widget-status success";
          status.innerHTML =
            'Posted. <a href="' +
            comment.html_url +
            '" target="_blank" rel="noopener">View on GitHub</a>';
          textarea.value = "";
          textarea.disabled = true;
          postBtn.style.display = "none";
        })
        .catch(function (err) {
          status.className = "comment-widget-status error";
          status.textContent = "Failed to post: " + err.message;
          postBtn.disabled = false;
          postBtn.textContent = "Post";
        });
    });

    var cancelBtn = document.createElement("button");
    cancelBtn.type = "button";
    cancelBtn.className = "comment-widget-cancel";
    cancelBtn.textContent = "Cancel";
    cancelBtn.addEventListener("click", onClose);

    var actions = document.createElement("div");
    actions.className = "comment-widget-actions";
    actions.appendChild(postBtn);
    actions.appendChild(cancelBtn);

    box.appendChild(textarea);
    box.appendChild(actions);
    box.appendChild(status);
    return box;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
