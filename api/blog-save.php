<?php
/**
 * Radiance Overseas — Blog Post API
 * Save/delete blog posts to blogs/posts.json
 * 
 * Protect with a simple password. Change BLOG_PASSWORD before deploying.
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

define('BLOG_PASSWORD', 'Radiance@2025');  // ← CHANGE THIS before going live
define('POSTS_FILE', __DIR__ . '/../blogs/posts.json');

// Read existing posts
function readPosts() {
    if (!file_exists(POSTS_FILE)) return [];
    $json = file_get_contents(POSTS_FILE);
    return json_decode($json, true) ?: [];
}

// Write posts
function writePosts($posts) {
    // Sort by date descending
    usort($posts, function($a, $b) {
        return strcmp($b['date'], $a['date']);
    });
    // Re-index IDs
    foreach ($posts as $i => &$p) {
        $p['id'] = $i + 1;
    }
    file_put_contents(POSTS_FILE, json_encode($posts, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
}

// Auth check
function checkAuth() {
    $input = json_decode(file_get_contents('php://input'), true);
    if (!$input || !isset($input['password']) || $input['password'] !== BLOG_PASSWORD) {
        http_response_code(401);
        echo json_encode(['error' => 'Invalid password']);
        exit;
    }
    return $input;
}

// GET — return all posts (public, no auth needed)
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $posts = readPosts();
    echo json_encode($posts);
    exit;
}

// POST — add or update a post
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = checkAuth();
    $action = $input['action'] ?? 'add';
    
    $posts = readPosts();
    
    if ($action === 'add') {
        // Validate required fields
        if (empty($input['title']) || empty($input['excerpt']) || empty($input['tag'])) {
            http_response_code(400);
            echo json_encode(['error' => 'title, excerpt, and tag are required']);
            exit;
        }
        
        $slug = strtolower(preg_replace('/[^a-z0-9]+/', '-', strtolower($input['title'])));
        $slug = substr($slug, 0, 60);
        
        $newPost = [
            'id' => count($posts) + 1,
            'slug' => $slug,
            'tag' => $input['tag'],
            'date' => $input['date'] ?? date('Y-m-d'),
            'title' => $input['title'],
            'excerpt' => $input['excerpt'],
            'image' => $input['image'] ?? 'https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=800&q=80',
            'author' => $input['author'] ?? 'Radiance Export Team',
        ];
        
        $posts[] = $newPost;
        writePosts($posts);
        
        echo json_encode(['success' => true, 'message' => 'Post added', 'post' => $newPost]);
        
    } elseif ($action === 'delete') {
        $deleteId = intval($input['id'] ?? 0);
        if ($deleteId <= 0) {
            http_response_code(400);
            echo json_encode(['error' => 'id is required for delete']);
            exit;
        }
        $posts = array_values(array_filter($posts, function($p) use ($deleteId) {
            return $p['id'] !== $deleteId;
        }));
        writePosts($posts);
        echo json_encode(['success' => true, 'message' => 'Post deleted']);
        
    } elseif ($action === 'update') {
        $updateId = intval($input['id'] ?? 0);
        foreach ($posts as &$p) {
            if ($p['id'] === $updateId) {
                if (!empty($input['title']))   $p['title'] = $input['title'];
                if (!empty($input['excerpt'])) $p['excerpt'] = $input['excerpt'];
                if (!empty($input['tag']))     $p['tag'] = $input['tag'];
                if (!empty($input['date']))    $p['date'] = $input['date'];
                if (!empty($input['image']))   $p['image'] = $input['image'];
                if (!empty($input['author']))  $p['author'] = $input['author'];
                $p['slug'] = strtolower(preg_replace('/[^a-z0-9]+/', '-', strtolower($p['title'])));
                break;
            }
        }
        writePosts($posts);
        echo json_encode(['success' => true, 'message' => 'Post updated']);
    }
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed']);
