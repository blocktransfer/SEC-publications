'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { changedFolders, publicationDate, approvedReviewers, run } = require('./published-examination-review.cjs');
const fence = String.fromCharCode(96).repeat(3);

test('reads metadata and rejects invalid publication dates', () => {
  assert.equal(publicationDate(fence + '\npublish: 15 Sep 2025\n' + fence), '2025-09-15');
  assert.equal(publicationDate('---\npublish: 2026-10-22\n---\n'), '2026-10-22');
  assert.equal(publicationDate('# publish: 2025-09-15'), null);
  assert.throws(() => publicationDate(fence + '\npublish: 31 Feb 2025\n' + fence), /Invalid/);
});

test('examines nested files and old paths of renamed files', () => {
  assert.deepEqual(changedFolders([
    { filename: 'examinations/response-8/imgs/new.png' },
    { filename: 'elsewhere/new.md', previous_filename: 'examinations/response-9/old.md' },
    { filename: 'examinations/LICENSE' }
  ]), ['response-8', 'response-9']);
});

test('only independent non-dismissed approvals on current head count', () => {
  assert.deepEqual(approvedReviewers([
    { id: 1, user: { login: 'author', type: 'User' }, state: 'APPROVED', commit_id: 'new' },
    { id: 2, user: { login: 'old', type: 'User' }, state: 'APPROVED', commit_id: 'old' },
    { id: 3, user: { login: 'removed', type: 'User' }, state: 'APPROVED', commit_id: 'new' },
    { id: 4, user: { login: 'removed', type: 'User' }, state: 'DISMISSED', commit_id: 'new' },
    { id: 5, user: { login: 'real', type: 'User' }, state: 'APPROVED', commit_id: 'new' }
  ], 'new', 'author'), ['real']);
});

function fake({ files, reviews = [], base = null, head = null, permission = 'write' }) {
  const statuses = [];
  const gh = {
    statuses,
    rest: {
      pulls: {
        get: async () => ({ data: { base: { ref: 'main', sha: 'base' }, head: { sha: 'head', repo: { owner: { login: 'blocktransfer' }, name: 'SEC-publications' } }, user: { login: 'author' } } }),
        listFiles() {}, listReviews() {}
      },
      repos: {
        createCommitStatus: async item => { statuses.push(item); },
        getContent: async ({ ref }) => {
          const source = ref === 'base' ? base : head;
          if (source === null) throw Object.assign(new Error('not found'), { status: 404 });
          return { data: { type: 'file', encoding: 'base64', content: Buffer.from(source).toString('base64') } };
        },
        getCollaboratorPermissionLevel: async () => ({ data: { permission } })
      }
    }
  };
  gh.paginate = async method => method === gh.rest.pulls.listFiles ? files : reviews;
  return gh;
}
const context = { repo: { owner: 'blocktransfer', repo: 'SEC-publications' }, payload: { pull_request: { number: 1 } }, serverUrl: 'https://github.com', runId: 10 };

test('fails when published folder is edited with no approval', async () => {
  const gh = fake({ files: [{ filename: 'examinations/response-8/imgs/new.png' }], base: fence + '\npublish: 15 Sep 2025\n' + fence });
  const failures = [];
  await run({ github: gh, context, core: { setFailed: value => failures.push(value) } });
  assert.deepEqual(gh.statuses.map(s => s.state), ['pending', 'failure']);
  assert.equal(failures.length, 1);
});

test('passes on fresh write-access approval', async () => {
  const gh = fake({ files: [{ filename: 'examinations/response-8/README.md' }], base: fence + '\npublish: 15 Sep 2025\n' + fence,
    reviews: [{ id: 1, user: { login: 'writer', type: 'User' }, state: 'APPROVED', commit_id: 'head' }] });
  await run({ github: gh, context, core: { setFailed: () => { throw new Error('should pass'); } } });
  assert.deepEqual(gh.statuses.map(s => s.state), ['pending', 'success']);
});

test('passes without approval if publication is future', async () => {
  const gh = fake({ files: [{ filename: 'examinations/upcoming/README.md' }], head: fence + '\npublish: 15 Sep 2999\n' + fence });
  await run({ github: gh, context, core: { setFailed: () => { throw new Error('should pass'); } } });
  assert.deepEqual(gh.statuses.map(s => s.state), ['pending', 'success']);
});
