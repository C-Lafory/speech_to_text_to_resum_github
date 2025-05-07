package middleware

import (
	"net"
	"net/http"
	"sync"
	"time"

	"golang.org/x/time/rate"
)

type client struct {
	limiter  *rate.Limiter
	lastSeen time.Time
}

var (
	mu          sync.Mutex
	clientsIP   = make(map[string]*client)
	clientsUser = make(map[string]*client)
	cleanupInterval = time.Minute * 5
)

// Nettoie les anciens clients pour libérer de la mémoire
func init() {
	go cleanupClients()
}

func getClientIPLimiter(ip string) *rate.Limiter {
	mu.Lock()
	defer mu.Unlock()

	c, exists := clientsIP[ip]
	if !exists {
		limiter := rate.NewLimiter(1, 5) // 1 req/sec, burst de 5
		clientsIP[ip] = &client{limiter, time.Now()}
		return limiter
	}

	c.lastSeen = time.Now()
	return c.limiter
}

func GetClientUsernameLimiter(username string) *rate.Limiter {
	mu.Lock()
	defer mu.Unlock()

	c, exists := clientsUser[username]
	if !exists {
		limiter := rate.NewLimiter(1, 3) // 1 req/sec, burst de 3 pour un username
		clientsUser[username] = &client{limiter, time.Now()}
		return limiter
	}

	c.lastSeen = time.Now()
	return c.limiter
}

func cleanupClients() {
	for {
		time.Sleep(cleanupInterval)

		mu.Lock()
		for ip, c := range clientsIP {
			if time.Since(c.lastSeen) > time.Minute*10 {
				delete(clientsIP, ip)
			}
		}
		for user, c := range clientsUser {
			if time.Since(c.lastSeen) > time.Minute*10 {
				delete(clientsUser, user)
			}
		}
		mu.Unlock()
	}
}

// Middleware à utiliser dans le handler
func RateLimitIP(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ip, _, _ := net.SplitHostPort(r.RemoteAddr)
		limiter := getClientIPLimiter(ip)

		if !limiter.Allow() {
			http.Error(w, "🛑 Trop de requêtes. Réessaie plus tard.", http.StatusTooManyRequests)
			return
		}
		next.ServeHTTP(w, r)
	})
}
