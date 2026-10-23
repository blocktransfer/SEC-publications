'use strict';

const STATUS_CONTEXT = 'published-examination-approval';
const MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];

function changedFolders(files) {
  const folders = new Set();
  for (const file of files) {
    for (const path of [file.filename, file.previous_filename]) {
      const match = /^examinations\/([^/]+)\/.+/.exec(path || '');
      if (match) folders.add(match[1]);
    }
  }
  return [...folders].sort();
}

function publicationDate(markdown) {
  // Only leading metadata can designate a published record.
  const fence = String.fromCharCode(96).repeat(3);
  const fenced = markdown.startsWith(fence);
  let block = null;
  if (fenced) {
    const end = markdown.indexOf('\n' + fence, fence.length);
    if (end >= 0) block = markdown.slice(markdown.indexOf('\n') + 1, end);
  } else if (markdown.startsWith('---')) {
    const end = markdown.indexOf('\n---', 3);
    if (end >= 0) block = markdown.slice(4, end);
  }
  if (block === null) return null;
  const match = /^\s*publish\s*:\s*(.*?)\s*$/im.exec(block);
  if (!match) return null;
  const value = match[1].trim().replace(/^['"]|['"]$/g, '');
  const iso = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  const named = /^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$/.exec(value);
  let y, m, d;
  if (iso) {
    y = Number(iso[1]); m = Number(iso[2]); d = Number(iso[3]);
  } else if (named) {
    d = Number(named[1]); m = MONTHS.indexOf(named[2].toLowerCase().slice(0, 3)) + 1; y = Number(named[3]);
  } else {
    return null;
  }
  const parsed = new Date(Date.UTC(y, m - 1, d));
  if (!m || parsed.getUTCFullYear() !== y || parsed.getUTCMonth() !== m - 1 || parsed.getUTCDate() !== d) {
    return null;
  }
  return parsed.toISOString().slice(0, 10);
}

function approvedReviewers(reviews, headSha, author) {
  const decisions = new Map();
  for (const review of [...reviews].sort((a, b) => a.id - b.id)) {
    const login = review.user?.login;
    if (!login || login.toLowerCase() === author.toLowerCase()) continue;
    if (['APPROVED', 'CHANGES_REQUESTED', 'DISMISSED'].includes(review.state)) {
      decisions.set(login.toLowerCase(), review);
    }
  }
  return [...decisions.values()].filter(review =>
    review.state === 'APPROVED' && review.commit_id === headSha &&
    review.user.type !== 'Bot' && !review.user.login.endsWith('[bot]')
  ).map(review => review.user.login);
}

async function readReadme(github, owner, repo, sha, folder) {
  try {
    const { data } = await github.rest.repos.getContent({
      owner, repo, path: 'examinations/' + folder + '/README.md', ref: sha
    });
    if (Array.isArray(data) || data.type !== 'file' || data.encoding !== 'base64') {
      throw new Error('Unexpected README response: ' + folder);
    }
    return Buffer.from(data.content.replace(/\s/g, ''), 'base64').toString('utf8');
  } catch (error) {
    if (error.status === 404) return null;
    throw error;
  }
}

async function run({ github, context, core, pull_number }) {
  const { owner, repo } = context.repo;
  const prNumber = pull_number || context.payload.pull_request?.number;
  if (!prNumber) throw new Error('No PR associated with event');
  const { data: pr } = await github.rest.pulls.get({ owner, repo, pull_number: prNumber });
  if (pr.base.ref !== 'main') return;
  const sha = pr.head.sha;
  async function status(state, description) {
    await github.rest.repos.createCommitStatus({
      owner, repo, sha, context: STATUS_CONTEXT, state,
      description: description.slice(0, 140),
      target_url: context.serverUrl + '/' + owner + '/' + repo + '/actions/runs/' + context.runId
    });
  }
  try {
    const files = await github.paginate(github.rest.pulls.listFiles, {
      owner, repo, pull_number: prNumber, per_page: 100
    });
    if (files.length >= 3000) throw new Error('PR has 3000+ files: cannot verify complete change set');
    const today = new Date().toISOString().slice(0, 10);
    const protectedFolders = [];
    for (const folder of changedFolders(files)) {
      const baseReadme = await readReadme(github, owner, repo, pr.base.sha, folder);
      const headReadme = await readReadme(github, pr.head.repo.owner.login, pr.head.repo.name, sha, folder);
      const dates = [baseReadme, headReadme].filter(value => value !== null).map(publicationDate);
      if (dates.some(date => date !== null && date < today)) protectedFolders.push(folder);
    }
    if (!protectedFolders.length) {
      await status('success', 'No publication approval required');
      return;
    }
    await status('pending', 'Checking contributor approvals for published examinations');
    const reviews = await github.paginate(github.rest.pulls.listReviews, {
      owner, repo, pull_number: prNumber, per_page: 100
    });
    const eligible = [];
    for (const reviewer of approvedReviewers(reviews, sha, pr.user.login)) {
      const { data } = await github.rest.repos.getCollaboratorPermissionLevel({
        owner, repo, username: reviewer
      });
      if (['admin', 'write'].includes(data.permission)) eligible.push(reviewer);
    }
    if (eligible.length) {
      await status('success', 'Approved by ' + eligible[0] + ': ' + protectedFolders.join(', '));
    } else {
      await status('failure', 'Needs contributor approval: ' + protectedFolders.join(', '));
      core.setFailed('Changes to published folders ' + protectedFolders.join(', ') +
        ' need a current approving review from a different human with write access on SHA ' + sha);
    }
  } catch (error) {
    await status('failure', 'Unable to verify examination approvals');
    throw error;
  }
}

module.exports = { run, changedFolders, publicationDate, approvedReviewers };
