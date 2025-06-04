// Caution! Be sure you understand the caveats before publishing an application with service worker enabled.
// Consider disabling service worker registration if you don't need the offline support it provides. 
// For more info, see https://aka.ms/blazor-PWA

const CACHE_VERSION = '{{POST_BUILD_ENTRIES_HASH}}'; // This will be replaced by the build process
const ASSETS_TO_CACHE = [
    './',
    'index.html',
    'css/app.css',
    'css/bootstrap/bootstrap.min.css',
    'manifest.json'
    // Add other assets like images, fonts if they are not covered by `cacheName` logic below
    // 'icon-192.png',
    // 'icon-512.png',
];
const CACHE_NAME_PREFIX = 'offline-cache-';
const CACHE_NAME = `${CACHE_NAME_PREFIX}${CACHE_VERSION}`;

self.addEventListener('install', event => {
    console.log('[Service Worker] Install event');
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('[Service Worker] Pre-caching offline pages and assets');
            return cache.addAll(ASSETS_TO_CACHE.map(url => new Request(url, { cache: 'reload' })));
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', event => {
    console.log('[Service Worker] Activate event');
    event.waitUntil(
        caches.keys().then(async (keys) => {
            for (const key of keys) {
                if (key.startsWith(CACHE_NAME_PREFIX) && key !== CACHE_NAME) {
                    console.log(`[Service Worker] Deleting old cache: ${key}`);
                    await caches.delete(key);
                }
            }
        })
    );
    console.log('[Service Worker] Claiming clients');
    return self.clients.claim(); 
});

self.addEventListener('fetch', event => {
    if (event.request.method !== 'GET' || event.request.url.startsWith('chrome-extension://')) {
        return; 
    }

    event.respondWith(
        caches.open(CACHE_NAME).then(cache => {
            return cache.match(event.request).then(response => {
                if (response) {
                    return response;
                }
                return fetch(event.request).then(networkResponse => {
                    if (networkResponse && networkResponse.status === 200 && networkResponse.type !== 'opaque') {
                        // Only cache if it's a valid, non-opaque response
                        // cache.put(event.request, networkResponse.clone());
                    }
                    return networkResponse;
                });
            }).catch(error => {
                console.error(`[Service Worker] Fetch error for ${event.request.url}:`, error);
                if (event.request.mode === 'navigate') {
                    return caches.match('index.html');
                }
                throw error;
            });
        })
    );
});
/* Manifest version: 0CnNxN5/ */
