#include <iostream>
#include <unordered_set>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <curl/curl.h>
#include <stdexcept>

// Helper function to download the file contents from the URL
size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::unordered_set<long long> download_numbers(const std::string& url) {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;
    
    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);

        if(res != CURLE_OK) {
            std::cerr << "Failed to download file: " << curl_easy_strerror(res) << std::endl;
            exit(1);
        }
    }

    // Parse the readBuffer into a set of integers
    std::unordered_set<long long> numbers;
    std::istringstream stream(readBuffer);
    std::string line;
    while (std::getline(stream, line)) {
        try {
            // Ignore empty lines
            if (line.empty()) continue;

            // Convert each line to a long long integer
            long long number = std::stoll(line);
            numbers.insert(number);
        } catch (const std::invalid_argument& e) {
            std::cerr << "Invalid number format in line: " << line << std::endl;
        } catch (const std::out_of_range& e) {
            std::cerr << "Number out of range in line: " << line << std::endl;
        }
    }

    return numbers;
}

int two_sum_variant(const std::unordered_set<long long>& numbers, int target_min, int target_max) {
    std::unordered_set<int> valid_targets;

    // Iterate over each number in `numbers`
    for (long long x : numbers) {
        // Check potential values of `y` such that x + y falls within the target range
        for (int t = target_min; t <= target_max; ++t) {
            long long y = t - x;
            // Ensure y is distinct from x and exists in the set
            if (y != x && numbers.find(y) != numbers.end()) {
                valid_targets.insert(t);
                // No need to break, as we want to find all valid targets
            }
        }
    }

    return valid_targets.size();
}

int main() {
    // URL of the input file
    std::string url = "https://d3c33hcgiwev3.cloudfront.net/_6ec67df2804ff4b58ab21c12edcb21f8_algo1-programming_prob-2sum.txt?Expires=1730332800&Signature=XG5zTKBt5vC~sFModXc6ALHNcW02~z8Oh5Tu1efBGk00CcK1sy4p0V6MIBznozKyHwipGf~nCZm9LpMYfLhVGlFVk91Inyx0P33eDEYMgW1VQcvfdvdIaVEtccl9pniztlavqXPVPypD~dmrwqDEyd0WrdCGvwqCnAgz9CmgLv8_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A";
    
    // Download the numbers from the URL
    std::unordered_set<long long> numbers = download_numbers(url);

    // Define the target range as [-10000, 10000]
    int target_min = -10000;
    int target_max = 10000;

    // Run the two-sum variant algorithm and get the result
    int result = two_sum_variant(numbers, target_min, target_max);
    
    // Print the result
    std::cout << result << std::endl;

    return 0;
}
