// In-preview commenting widget.
//
// Adds a "Comment" button next to every ID-only heading (BR-006, DEC-002,
// ...) that comment-map.json (generate_comment_map.py) knows a source
// line for. "Post" calls GitHub's REST API directly from the browser,
// using the reviewer's own token (below) -- CORS confirmed working
// against a real PR, not just assumed.
//
// Tries a real inline PR review comment first (anchored to the exact
// line). GitHub only allows that when the line is part of the PR's diff
// hunks, though -- confirmed live: most ID headings in a real document
// are NOT part of any given PR's diff (only what that PR actually
// changed is), so this is the common case, not an edge case. When
// GitHub rejects the line for that reason, this falls back to a general
// (not line-anchored) PR comment, prefixed with the ID it's about --
// still a real GitHub comment, still readable by resolve-review-decisions
// (which already treats general comments as first-class input), just
// not anchored to an exact line GitHub won't allow anyway.
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

  function apiHeaders() {
    return {
      Authorization: "Bearer " + getToken(),
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "Content-Type": "application/json",
    };
  }

  function githubError(err, status) {
    var message = (err && err.message) || "GitHub API error " + status;
    var e = new Error(message);
    // GitHub's specific shape when the requested line isn't part of the
    // PR's diff hunks -- confirmed against a real 422 while testing this
    // live: {"errors":[{"field":"pull_request_review_thread.line",
    // "message":"could not be resolved"}]}. Most ID headings in a real
    // document are NOT part of any given PR's diff (only what that PR
    // actually changed is), so this isn't an edge case -- it's the
    // common case, and needs a real fallback, not just a surfaced error.
    e.lineNotInDiff =
      !!err &&
      Array.isArray(err.errors) &&
      err.errors.some(function (x) {
        return x.field === "pull_request_review_thread.line";
      });
    return e;
  }

  function parseErrorBody(r) {
    return r.json().catch(function () {
      return {};
    });
  }

  // Real inline PR review comment, anchored to an exact line -- only
  // succeeds when that line is part of the PR's diff (GitHub's own
  // constraint, not something this widget can relax).
  function postInlineComment(target, body) {
    var url =
      "https://api.github.com/repos/" + target.repo + "/pulls/" + target.prNumber + "/comments";
    return fetch(url, {
      method: "POST",
      headers: apiHeaders(),
      body: JSON.stringify({
        body: body,
        commit_id: target.commitSha,
        path: target.path,
        line: target.line,
        side: "RIGHT",
      }),
    }).then(function (r) {
      if (!r.ok) return parseErrorBody(r).then(function (err) { throw githubError(err, r.status); });
      return r.json();
    });
  }

  // General (not line-anchored) PR comment -- PRs are issues in GitHub's
  // API, so this is the ordinary issue-comments endpoint. Used as the
  // fallback whenever the target line isn't part of the diff; prefixed
  // with the ID so it's still traceable back to what it's about, same
  // as resolve-review-decisions already expects for general comments.
  function postGeneralComment(target, body) {
    var url =
      "https://api.github.com/repos/" + target.repo + "/issues/" + target.prNumber + "/comments";
    var prefixed = "Re: `" + target.id + "`: " + body;
    return fetch(url, {
      method: "POST",
      headers: apiHeaders(),
      body: JSON.stringify({ body: prefixed }),
    }).then(function (r) {
      if (!r.ok) return parseErrorBody(r).then(function (err) { throw githubError(err, r.status); });
      return r.json();
    });
  }

  function filesChangedUrl(target) {
    return "https://github.com/" + target.repo + "/pull/" + target.prNumber + "/files";
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

      attemptPost(body);
    });

    function showSuccess(comment, note) {
      status.className = "comment-widget-status success";
      status.innerHTML =
        note + ' <a href="' + comment.html_url + '" target="_blank" rel="noopener">View on GitHub</a>';
      textarea.value = "";
      textarea.disabled = true;
      postBtn.style.display = "none";
    }

    function showChoice(body) {
      // The line isn't part of this PR's diff, so GitHub can't place an
      // inline comment there -- not a failure, a real choice for the
      // reviewer: post as an ordinary PR comment (still traceable, still
      // read by resolve-review-decisions), or go leave a true inline
      // comment on GitHub themselves, e.g. after expanding context to a
      // nearby line that IS in the diff.
      status.className = "comment-widget-status choice";
      status.innerHTML =
        "This section isn't part of the current diff, so GitHub can't place an inline comment there.";

      var generalBtn = document.createElement("button");
      generalBtn.type = "button";
      generalBtn.className = "comment-widget-post";
      generalBtn.textContent = "Post as general comment";
      generalBtn.addEventListener("click", function () {
        generalBtn.disabled = true;
        postGeneralComment(target, body)
          .then(function (comment) {
            showSuccess(comment, "Posted as a general PR comment.");
          })
          .catch(function (err) {
            status.className = "comment-widget-status error";
            status.textContent = "Failed to post: " + err.message;
          });
      });

      var githubLink = document.createElement("a");
      githubLink.className = "comment-widget-post";
      githubLink.href = filesChangedUrl(target);
      githubLink.target = "_blank";
      githubLink.rel = "noopener";
      githubLink.textContent = "Open on GitHub instead";

      var choiceActions = document.createElement("div");
      choiceActions.className = "comment-widget-actions";
      choiceActions.appendChild(generalBtn);
      choiceActions.appendChild(githubLink);
      status.appendChild(choiceActions);

      postBtn.disabled = false;
      postBtn.textContent = "Post";
    }

    function attemptPost(body) {
      postBtn.disabled = true;
      postBtn.textContent = "Posting…";
      status.className = "comment-widget-status";
      status.textContent = "";

      postInlineComment(target, body)
        .then(function (comment) {
          showSuccess(comment, "Posted.");
        })
        .catch(function (err) {
          if (err.lineNotInDiff) {
            showChoice(body);
            return;
          }
          status.className = "comment-widget-status error";
          status.textContent = "Failed to post: " + err.message;
          postBtn.disabled = false;
          postBtn.textContent = "Post";
        });
    }

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
