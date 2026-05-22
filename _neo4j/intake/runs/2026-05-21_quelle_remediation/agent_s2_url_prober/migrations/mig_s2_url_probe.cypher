// Agent S2 - URL probe writes
// Owner: agent_s2/url-probe
// Scope: only url_* properties on :ExternalLink plus :DataIssue for unreachable URLs.

// S2.A - write probe results to every :ExternalLink node for one URL.
MATCH (ext:ExternalLink {id: $external_link_id})
SET ext.url_status                 = $url_status,
    ext.url_http_code              = $url_http_code,
    ext.url_final_url              = $url_final_url,
    ext.url_redirect_chain         = $url_redirect_chain,
    ext.url_content_type           = $url_content_type,
    ext.url_content_length_bytes   = $url_content_length_bytes,
    ext.url_last_modified_header   = $url_last_modified_header,
    ext.url_server_header          = $url_server_header,
    ext.url_response_headers       = $url_response_headers,
    ext.url_last_checked_at        = date(),
    ext.url_probe_attempts         = coalesce(ext.url_probe_attempts, 0) + 1,
    ext.url_probe_duration_ms      = $url_probe_duration_ms,
    ext.url_user_agent             = $url_user_agent,
    ext.url_body_cache_path        = $url_body_cache_path,
    ext.url_body_cache_format      = $url_body_cache_format,
    ext.url_body_md5               = $url_body_md5,
    ext.url_wayback_snapshot       = $url_wayback_snapshot,
    ext.url_wayback_timestamp      = $url_wayback_timestamp,
    ext.url_wayback_attempted      = $url_wayback_attempted,
    ext.migration_origin           = CASE
      WHEN coalesce(ext.migration_origin, '') CONTAINS 'mig_s2_url_probe'
        THEN ext.migration_origin
      WHEN ext.migration_origin IS NULL OR ext.migration_origin = ''
        THEN 'mig_s2_url_probe'
      ELSE ext.migration_origin + ' | mig_s2_url_probe'
    END;

// S2.B - emit DataIssue for dead, blocked, or unsupported URLs.
WITH $url_status AS status, $url AS url, $external_link_id AS eid,
     $url_wayback_snapshot AS wayback
WHERE status IN [
  'dead_4xx',
  'dead_5xx',
  'timeout',
  'dns_failure',
  'tls_failure',
  'blocked_by_robots',
  'unsupported_scheme'
]
MATCH (ext:ExternalLink {id: eid})
MERGE (i:DataIssue {id: 'di_url_' + status + '__' + eid})
ON CREATE SET
  i.kind = CASE status
    WHEN 'dead_4xx' THEN 'url_unreachable_4xx'
    WHEN 'dead_5xx' THEN 'url_unreachable_5xx'
    WHEN 'timeout' THEN 'url_timeout'
    WHEN 'dns_failure' THEN 'url_dns_failure'
    WHEN 'tls_failure' THEN 'url_tls_failure'
    WHEN 'blocked_by_robots' THEN 'url_blocked_by_robots'
    WHEN 'unsupported_scheme' THEN 'url_unsupported_scheme'
    ELSE 'url_unknown_status' END,
  i.severity = CASE status
    WHEN 'dead_4xx' THEN 'medium'
    WHEN 'dead_5xx' THEN 'medium'
    WHEN 'dns_failure' THEN 'medium'
    WHEN 'tls_failure' THEN 'medium'
    WHEN 'unsupported_scheme' THEN 'low'
    ELSE 'low' END,
  i.ref_label = 'ExternalLink',
  i.ref_id = eid,
  i.url = url,
  i.found_at = date(),
  i.found_by = 's2_url_probe',
  i.status = 'open',
  i.resolution_note = 'URL not reachable (' + status + '). Wayback fallback: ' +
                      coalesce(wayback, 'unavailable'),
  i.migration_origin = 'mig_s2_url_probe'
ON MATCH SET
  i.url = url,
  i.resolution_note = 'URL not reachable (' + status + '). Wayback fallback: ' +
                      coalesce(wayback, 'unavailable')
MERGE (i)-[:CONCERNS]->(ext);
